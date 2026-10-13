"""On-disk response cache. Serves two purposes:

1. quota protection - an identical search / fetch / LLM call is never paid for twice;
2. reproducibility - `replay` mode re-runs the whole pipeline from recorded responses, offline.

Modes:  auto    read cache, call the network on a miss, store the result (default)
        replay  read only; a miss raises CacheMiss (no network, no keys needed)
        refresh ignore existing entries and overwrite them
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import threading
from pathlib import Path
from typing import Any


class CacheMiss(RuntimeError):
    pass


class Cache:
    def __init__(self, root: str | Path, mode: str = "auto"):
        if mode not in ("auto", "replay", "refresh"):
            raise ValueError(f"bad cache mode {mode!r}")
        self.root = Path(root)
        self.mode = mode
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    @staticmethod
    def key(params: dict[str, Any]) -> str:
        blob = json.dumps(params, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:24]

    def _path(self, ns: str, params: dict[str, Any]) -> Path:
        return self.root / ns / f"{self.key(params)}.json"

    def get(self, ns: str, params: dict[str, Any]) -> Any | None:
        if self.mode == "refresh":
            return None
        p = self._path(ns, params)
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                with self._lock:
                    self.hits += 1
                return data["value"]
            except (OSError, ValueError, KeyError):
                return None  # corrupt entry -> treated as a miss
        return None

    def require_network_allowed(self, what: str) -> None:
        if self.mode == "replay":
            raise CacheMiss(f"replay mode: no recorded response for {what}")
        with self._lock:
            self.misses += 1

    def put(self, ns: str, params: dict[str, Any], value: Any) -> None:
        p = self._path(ns, params)
        p.parent.mkdir(parents=True, exist_ok=True)
        payload = {"request": params, "value": value}
        fd, tmp = tempfile.mkstemp(dir=p.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=1)
            os.replace(tmp, p)  # atomic: a crash never leaves a half-written entry
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
