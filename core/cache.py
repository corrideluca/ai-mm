"""Simple file-based cache to reduce API calls and save tokens."""

import json
import time
from datetime import datetime
from pathlib import Path
from core.config import config

CACHE_DIR = Path(__file__).parent.parent / ".cache"
CACHE_DIR.mkdir(exist_ok=True)


def _cache_path(key: str) -> Path:
    return CACHE_DIR / f"{key}.json"


def get(key: str) -> dict | None:
    """Get cached value if not expired."""
    path = _cache_path(key)
    if not path.exists():
        return None

    data = json.loads(path.read_text())
    if time.time() - data["ts"] > config.cache_ttl_seconds:
        path.unlink()
        return None

    return data["value"]


def set(key: str, value) -> None:
    """Cache a value."""
    path = _cache_path(key)
    path.write_text(json.dumps({"ts": time.time(), "value": value}, default=str))


def clear() -> None:
    """Clear all cache."""
    for f in CACHE_DIR.glob("*.json"):
        f.unlink()
