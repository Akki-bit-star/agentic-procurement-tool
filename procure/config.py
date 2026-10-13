"""Config loading. Non-secret settings live in YAML; secrets come from the environment only."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, model_validator

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"


class SearchCfg(BaseModel):
    provider: str = "serper"
    country: str = "in"
    results_per_query: int = 10
    max_search_calls_total: int = 60
    max_queries_per_material_per_tier: int = 3
    max_places_calls_per_material: int = 1
    max_pages_fetched_per_vendor: int = 2
    max_followup_pages_per_vendor: int = 3
    max_vendors_verified_per_material_per_tier: int = 8
    fetch_timeout_s: int = 15
    fetch_max_bytes: int = 600000


class AgentCfg(BaseModel):
    enabled: bool = False                    # model-directed research loop instead of the rule-driven discovery/verify
    max_steps: int = 10                      # model turns per (material x geography) agent
    min_vendors_per_tier: int = 4            # below this the rule-driven discovery backstop also runs for that geography
    max_searches: int = 4                    # search/places calls per agent (cached queries are free)
    max_reads: int = 8                       # page reads per agent
    max_output_tokens: int = 1500
    digest_chars: int = 1800                 # size of a read_page digest (keep small for low tokens-per-minute plans)


class LLMCfg(BaseModel):
    provider: str = "anthropic"              # anthropic | openai_compat | none
    base_url: str | None = None
    api_key_env: str | None = None           # NAME of the env var that holds the key (never the key itself)
    fast_model: str = "claude-haiku-5-5"
    strong_model: str = "claude-sonnet-5-5"
    fallback_models: list[str] = Field(default_factory=list)   # tried in order when a model's daily quota is exhausted
    extra_params: dict = Field(default_factory=dict)           # provider tuning knobs merged into each request (e.g. reasoning_effort)
    max_calls_total: int = 120
    requests_per_minute: int | None = None   # client-side pacing for rate-limited plans
    agent: AgentCfg = Field(default_factory=AgentCfg)


class ShortlistCfg(BaseModel):
    per_tier_per_material: int = 5
    min_confidence: str = "LOW"
    include_unverified: bool = True


class LocationCfg(BaseModel):
    city: str = "Ahmedabad"
    state: str = "Gujarat"
    country: str = "India"


class RunConfig(BaseModel):
    default_unit: str = "tonnes"
    strict: bool = False
    procurement_location: LocationCfg = Field(default_factory=LocationCfg)
    search: SearchCfg = Field(default_factory=SearchCfg)
    llm: LLMCfg = Field(default_factory=LLMCfg)
    shortlist: ShortlistCfg = Field(default_factory=ShortlistCfg)
    weights: dict[str, float]
    match_score: dict[str, float]
    source_reliability: dict[str, float]
    bulk_scores: dict[str, float] = Field(default_factory=dict)
    large_order_tonnes: float = 100
    non_vendor_domains: list[str] = Field(default_factory=list)
    marketplace_domains: list[str] = Field(default_factory=list)
    tolerated_standards_near_match: list[str] = Field(default_factory=list)
    global_import_checks: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _weights_sum(self) -> "RunConfig":
        total = sum(self.weights.values())
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"ranking weights must sum to 1.0, got {total}")
        return self


def load_dotenv_file(path: Path | None = None) -> None:
    """Tiny .env reader (no dependency on shell state). Real env vars win."""
    path = path or ROOT / ".env"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def load_config(path: str | Path | None = None, overrides: dict | None = None) -> RunConfig:
    load_dotenv_file()
    p = Path(path) if path else CONFIG_DIR / "default.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    for k, v in (overrides or {}).items():
        # dotted override, e.g. "search.provider"
        node = data
        parts = k.split(".")
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = v
    return RunConfig(**data)


def llm_preset_overrides(name: str) -> dict:
    """Flatten a provider preset (config/llm_presets.yaml) into dotted `llm.*` overrides for load_config()."""
    presets = yaml.safe_load((CONFIG_DIR / "llm_presets.yaml").read_text(encoding="utf-8"))
    if name not in presets:
        raise ValueError(f"unknown LLM preset {name!r}; available: {sorted(presets)}")
    return {f"llm.{k}": v for k, v in presets[name].items()}


def llm_preset_names() -> list[str]:
    presets = yaml.safe_load((CONFIG_DIR / "llm_presets.yaml").read_text(encoding="utf-8"))
    return sorted(presets)


def secret(name: str) -> str | None:
    load_dotenv_file()
    v = os.environ.get(name)
    return v or None


@lru_cache(maxsize=1)
def load_gazetteer() -> dict:
    return yaml.safe_load((CONFIG_DIR / "gazetteer.yaml").read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_standards() -> dict:
    return yaml.safe_load((CONFIG_DIR / "standards_is1239.yaml").read_text(encoding="utf-8"))
