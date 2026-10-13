"""Safe page fetcher.

Search results are untrusted URLs, so fetching them is a security surface:
  * http/https only; every hop (incl. redirects) must resolve to a public IP  -> SSRF guard
  * robots.txt is honoured; per-host politeness delay
  * hard size / time limits; non-HTML content is skipped, not guessed at
  * page text is DATA. It is never executed or treated as instructions (see agents/verify.py).
"""
from __future__ import annotations

import ipaddress
import re
import socket
import threading
import time
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup

from .cache import Cache, CacheMiss
from .context import RunContext
from .models import Page

UA = "ProcureAgent/0.1 (+vendor-research prototype; respects robots.txt)"
MAX_REDIRECTS = 3
_PER_HOST_DELAY_S = 0.7


def is_public_url(url: str) -> tuple[bool, str]:
    p = urlparse(url)
    if p.scheme not in ("http", "https"):
        return False, f"scheme {p.scheme!r} not allowed"
    host = p.hostname
    if not host:
        return False, "no host"
    try:
        infos = socket.getaddrinfo(host, p.port or (443 if p.scheme == "https" else 80), proto=socket.IPPROTO_TCP)
    except socket.gaierror as e:
        return False, f"dns failure: {e}"
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                or ip.is_multicast or ip.is_unspecified):
            return False, f"non-public address {ip}"
    return True, "ok"


def parse_html(html: str, base_url: str) -> dict:
    """text + title + og:site_name + same-site contact/about links."""
    soup = BeautifulSoup(html, "lxml")
    title = soup.title.get_text(" ", strip=True) if soup.title else None
    og = soup.find("meta", attrs={"property": "og:site_name"})
    site_name = og["content"].strip() if og and og.get("content") else None
    host = urlparse(base_url).netloc
    links: list[str] = []
    for a in soup.find_all("a", href=True):
        h = a["href"].strip()
        if h.lower().startswith(("tel:", "mailto:", "javascript:", "#")):
            continue
        absu = urljoin(base_url, h)
        label = f"{a.get_text(' ', strip=True)} {h}".lower()
        if urlparse(absu).netloc == host and re.search(r"contact|about|reach|enquir", label) and absu not in links:
            links.append(absu)
    return {"text": html_to_text(html), "title": title, "site_name": site_name, "links": links[:6]}


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    contact_bits: list[str] = []
    for a in soup.find_all("a", href=True):
        h = a["href"].strip()
        if h.lower().startswith(("tel:", "mailto:")):
            contact_bits.append(h)
    for t in soup(["script", "style", "noscript", "svg", "iframe"]):
        t.decompose()
    text = soup.get_text("\n")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text).strip()
    if contact_bits:
        text += "\n[links] " + " | ".join(dict.fromkeys(contact_bits))
    return text


class Fetcher:
    def __init__(self, ctx: RunContext, cache: Cache):
        self.ctx, self.cache = ctx, cache
        self._client = httpx.Client(timeout=ctx.cfg.search.fetch_timeout_s, follow_redirects=False,
                                    headers={"User-Agent": UA, "Accept": "text/html,text/plain;q=0.9"})
        self._blocked: dict[str, str] = {}
        self._robots: dict[str, RobotFileParser | None] = {}
        self._last_hit: dict[str, float] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ robots / politeness
    def _allowed(self, url: str) -> bool:
        p = urlparse(url)
        origin = f"{p.scheme}://{p.netloc}"
        with self._lock:
            known = origin in self._robots
            rp = self._robots.get(origin)
        if not known:
            rp = None
            try:
                ok, _ = is_public_url(origin)
                if ok:
                    r = self._client.get(origin + "/robots.txt")
                    if r.status_code == 200 and "text" in r.headers.get("content-type", "text"):
                        rp = RobotFileParser()
                        rp.parse(r.text.splitlines())
            except Exception:  # noqa: BLE001 - unreachable robots.txt => allowed (standard behaviour)
                rp = None
            with self._lock:
                self._robots[origin] = rp
        return True if rp is None else rp.can_fetch(UA, url)

    def _polite_wait(self, host: str) -> None:
        with self._lock:
            now = time.monotonic()
            wait = self._last_hit.get(host, 0) + _PER_HOST_DELAY_S - now
            self._last_hit[host] = now + max(wait, 0)
        if wait > 0:
            time.sleep(wait)

    # ------------------------------------------------------------------ main
    def fetch(self, url: str) -> Page:
        params = {"url": url}
        cached = self.cache.get("fetch", params)
        if cached is not None and (cached.get("ok") or self.cache.mode == "replay"):
            return Page(**cached)   # failed fetches are retried in auto mode, replayed in replay mode
        try:
            self.cache.require_network_allowed(f"fetch {url}")
        except CacheMiss as e:
            return Page(url=url, ok=False, error=str(e))
        host = (urlparse(url).hostname or "").removeprefix("www.")
        if host in self._blocked:       # a host that refused us once is not hammered with more requests
            return Page(url=url, ok=False, error=f"host blocked automated access earlier in this run ({self._blocked[host]}); not retried")
        page = self._fetch_network(url)
        if not page.ok and page.status in (401, 403, 429):
            self._blocked[host] = f"HTTP {page.status}"
        self.cache.put("fetch", params, page.model_dump(mode="json"))
        if not page.ok:
            self.ctx.log("fetch", "warn", f"fetch failed: {url} ({page.error})")
        return page

    def _fetch_network(self, url: str) -> Page:
        cfg = self.ctx.cfg.search
        current = url
        try:
            for _ in range(MAX_REDIRECTS + 1):
                ok, why = is_public_url(current)
                if not ok:
                    return Page(url=url, ok=False, error=f"blocked by SSRF guard: {why}")
                if not self._allowed(current):
                    return Page(url=url, ok=False, error="disallowed by robots.txt")
                self._polite_wait(urlparse(current).netloc)
                with self._client.stream("GET", current) as r:
                    if r.is_redirect:
                        loc = r.headers.get("location")
                        if not loc:
                            return Page(url=url, ok=False, status=r.status_code, error="redirect without location")
                        current = urljoin(current, loc)
                        continue
                    ctype = r.headers.get("content-type", "").lower()
                    if r.status_code >= 400:
                        return Page(url=url, ok=False, status=r.status_code, error=f"HTTP {r.status_code}")
                    if ctype and not any(t in ctype for t in ("html", "text/plain", "xml")):
                        return Page(url=url, ok=False, status=r.status_code, error=f"unsupported content-type {ctype}")
                    buf = bytearray()
                    for chunk in r.iter_bytes():
                        buf.extend(chunk)
                        if len(buf) > cfg.fetch_max_bytes:
                            break
                    html = bytes(buf).decode(r.encoding or "utf-8", errors="replace")
                    parsed = parse_html(html, current)
                    if len(parsed["text"]) < 80:
                        return Page(url=url, ok=False, status=r.status_code,
                                    error="page has no extractable text (JS-rendered or blocked)")
                    return Page(url=current, ok=True, status=r.status_code, **parsed)
            return Page(url=url, ok=False, error="too many redirects")
        except httpx.TimeoutException:
            return Page(url=url, ok=False, error="timeout")
        except Exception as e:  # noqa: BLE001
            return Page(url=url, ok=False, error=f"{type(e).__name__}: {e}")
