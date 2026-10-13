"""Run context: budgets (quota protection), structured run log, and progress events."""
from __future__ import annotations

import threading
from collections.abc import Callable
from typing import Any

from .config import RunConfig
from .models import RunLog


class BudgetExceeded(RuntimeError):
    pass


class Budget:
    """Hard caps on *network* calls. Cache hits are free and never counted, which is what
    protects the limited search quota across repeated runs."""

    def __init__(self, limits: dict[str, int]):
        self.limits = dict(limits)
        self.used: dict[str, int] = {k: 0 for k in limits}
        self._lock = threading.Lock()

    def spend(self, kind: str, n: int = 1) -> None:
        with self._lock:
            limit = self.limits.get(kind)
            if limit is not None and self.used.get(kind, 0) + n > limit:
                raise BudgetExceeded(f"{kind} budget exhausted ({self.used.get(kind, 0)}/{limit})")
            self.used[kind] = self.used.get(kind, 0) + n

    def remaining(self, kind: str) -> int | None:
        limit = self.limits.get(kind)
        return None if limit is None else limit - self.used.get(kind, 0)

    def snapshot(self) -> dict[str, str]:
        return {k: f"{self.used.get(k, 0)}/{v}" for k, v in self.limits.items()}


class RunContext:
    def __init__(self, cfg: RunConfig, budget: Budget | None = None,
                 on_event: Callable[[dict[str, Any]], None] | None = None):
        self.cfg = cfg
        self.budget = budget or Budget({
            "search": cfg.search.max_search_calls_total,
            "llm": cfg.llm.max_calls_total,
        })
        self.logs: list[RunLog] = []
        self._on_event = on_event
        self._lock = threading.Lock()

    def log(self, stage: str, level: str, message: str, **data: Any) -> None:
        entry = RunLog(stage=stage, level=level, message=message, data=data)
        with self._lock:
            self.logs.append(entry)
        self.emit({"type": "log", **entry.model_dump(mode="json")})

    def emit(self, event: dict[str, Any]) -> None:
        if self._on_event:
            try:
                self._on_event(event)
            except Exception:  # a broken UI listener must never break the run
                pass

    def stage(self, name: str, **data: Any) -> None:
        self.emit({"type": "stage", "stage": name, **data})
