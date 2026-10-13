"""Search providers behind one small interface.

To add Brave / Tavily: implement `RawSearchProvider` (two methods) and register it in
`PROVIDERS`. Caching, budgets, retries and logging are applied by `SearchService`, so
adapters stay ~30 lines and the rest of the system never imports a vendor module.
"""
from __future__ import annotations

import time
from typing import Protocol
from urllib.parse import quote_plus

import httpx

from ..cache import Cache, CacheMiss
from ..config import secret
from ..context import BudgetExceeded, RunContext
from ..models import SearchResult


class ProviderError(RuntimeError):
    pass


class RawSearchProvider(Protocol):
    name: str

    def search(self, query: str, *, country: str | None, num: int) -> list[SearchResult]: ...
    def places(self, query: str, *, country: str | None, num: int) -> list[SearchResult]: ...


class SerperProvider:
    """google.serper.dev - Google web results + Google Maps places (address / phone / website)."""
    name = "serper"
    BASE = "https://google.serper.dev"

    def __init__(self, api_key: str, timeout: float = 20.0):
        self._headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        self._client = httpx.Client(timeout=timeout)

    def _post(self, endpoint: str, body: dict) -> dict:
        last: Exception | None = None
        for attempt in range(3):
            try:
                r = self._client.post(f"{self.BASE}/{endpoint}", headers=self._headers, json=body)
                if r.status_code in (429, 500, 502, 503, 504):
                    last = ProviderError(f"HTTP {r.status_code}")
                    time.sleep(1.5 * (attempt + 1))
                    continue
                if r.status_code in (401, 403):
                    raise ProviderError(f"authentication rejected (HTTP {r.status_code}) - check SERPER_API_KEY")
                if r.status_code == 400 and "credit" in r.text.lower():
                    raise ProviderError("search credits exhausted")
                r.raise_for_status()
                return r.json()
            except httpx.TransportError as e:
                last = e
                time.sleep(1.5 * (attempt + 1))
        raise ProviderError(f"{endpoint} failed after retries: {last}")

    def search(self, query: str, *, country: str | None, num: int) -> list[SearchResult]:
        body: dict = {"q": query, "num": num}
        if country:
            body["gl"] = country
        data = self._post("search", body)
        out = []
        for i, o in enumerate(data.get("organic", []), start=1):
            if not o.get("link"):
                continue
            out.append(SearchResult(title=o.get("title", ""), url=o["link"], snippet=o.get("snippet", ""),
                                    position=o.get("position", i), query=query, provider=self.name))
        return out

    def places(self, query: str, *, country: str | None, num: int) -> list[SearchResult]:
        body: dict = {"q": query}
        if country:
            body["gl"] = country
        data = self._post("places", body)
        out = []
        for i, p in enumerate(data.get("places", [])[:num], start=1):
            # A map listing without a website still needs a citable source URL, otherwise its address could
            # never become evidence (the local dealers are exactly the ones with no website).
            if p.get("cid"):
                maps_url = f"https://www.google.com/maps?cid={p['cid']}"
            else:
                maps_url = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(f"{p.get('title', '')} {p.get('address', '')}")
            out.append(SearchResult(
                title=p.get("title", ""), url=p.get("website") or maps_url,
                snippet=p.get("category", "") or "", position=i, query=query, provider=self.name,
                address=p.get("address"), phone=p.get("phoneNumber"), website=p.get("website"),
                rating=p.get("rating")))
        return out


def _build_serper() -> RawSearchProvider:
    key = secret("SERPER_API_KEY")
    if not key:
        raise ProviderError("SERPER_API_KEY is not set (put it in .env or the environment)")
    return SerperProvider(key)


PROVIDERS = {"serper": _build_serper}


class SearchService:
    """What agents call. Adds cache, quota budget, error containment and logging."""

    def __init__(self, ctx: RunContext, cache: Cache, inner: RawSearchProvider | None):
        self.ctx, self.cache, self.inner = ctx, cache, inner
        # Keyed by the *configured* provider so live and replay runs share cache entries.
        self.provider_name = ctx.cfg.search.provider

    def _call(self, endpoint: str, query: str, country: str | None, num: int) -> list[SearchResult]:
        params = {"provider": self.provider_name, "endpoint": endpoint, "q": query, "country": country, "num": num}
        cached = self.cache.get("search", params)
        if cached is not None:
            return [SearchResult(**r) for r in cached]
        self.cache.require_network_allowed(f"{endpoint} '{query}'")  # raises CacheMiss in replay mode
        if self.inner is None:
            raise CacheMiss(f"no recorded response for {endpoint} '{query}' and no search key is configured "
                            "(set SERPER_API_KEY in .env to run new queries)")
        self.ctx.budget.spend("search")  # web and places calls draw from one quota
        fn = self.inner.places if endpoint == "places" else self.inner.search
        results = fn(query, country=country, num=num)
        self.cache.put("search", params, [r.model_dump(mode="json") for r in results])
        return results

    def search(self, query: str, *, country: str | None, num: int | None = None, stage: str = "search") -> list[SearchResult]:
        return self._safe("search", query, country, num, stage)

    def places(self, query: str, *, country: str | None, num: int = 10, stage: str = "search") -> list[SearchResult]:
        return self._safe("places", query, country, num, stage)

    def _safe(self, endpoint: str, query: str, country: str | None, num: int | None, stage: str) -> list[SearchResult]:
        """A failed search is logged and returns [] - it must never abort the run."""
        num = num or self.ctx.cfg.search.results_per_query
        try:
            res = self._call(endpoint, query, country, num)
            self.ctx.log(stage, "info", f"{endpoint}: '{query}' -> {len(res)} results", country=country)
            return res
        except BudgetExceeded:
            raise                       # the quota guard must stop the caller, not be swallowed as a failed search
        except Exception as e:  # noqa: BLE001 - containment is the point
            self.ctx.log(stage, "error", f"{endpoint} failed for '{query}': {e}", error_type=type(e).__name__)
            return []


def build_search_service(ctx: RunContext, cache: Cache) -> SearchService:
    name = ctx.cfg.search.provider
    if cache.mode == "replay" or name == "fixture":
        return SearchService(ctx, cache, None)
    if name not in PROVIDERS:
        raise ProviderError(f"unknown search provider {name!r}; available: {sorted(PROVIDERS)}")
    try:
        return SearchService(ctx, cache, PROVIDERS[name]())
    except ProviderError as e:
        # No key + normal cache mode: serve what was RECORDED (so a fresh clone can run the committed demo input end to end)
        # and report every query that has no recorded answer. `refresh` explicitly wants the network, so it still fails.
        if cache.mode == "auto" and "not set" in str(e):
            ctx.log("setup", "warn", f"{e}. Using recorded searches only: any query without a recorded response will fail "
                                     "and be reported (add the key to .env to run new queries).")
            return SearchService(ctx, cache, None)
        raise
