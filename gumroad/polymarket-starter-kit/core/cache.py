"""Simple file-based cache to avoid hitting Polymarket API too often.

Stores JSON in /tmp/polymarket_cache/ with 5-minute TTL.
"""

import json
import time
from pathlib import Path

CACHE_DIR = Path("/tmp/polymarket_cache")
CACHE_DIR.mkdir(exist_ok=True)
TTL = 300  # 5 minutes


def _path(key: str) -> Path:
    return CACHE_DIR / f"{key}.json"


def get(key: str):
    """Get cached value or None if expired/missing."""
    p = _path(key)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text())
        if time.time() - data["ts"] < TTL:
            return data["value"]
    except Exception:
        pass
    return None


def set(key: str, value) -> None:
    """Cache a value for TTL seconds."""
    _path(key).write_text(json.dumps({"ts": time.time(), "value": value}))


def clear(key: str = None) -> None:
    """Clear a specific key or all cache."""
    if key:
        _path(key).unlink(missing_ok=True)
    else:
        for f in CACHE_DIR.glob("*.json"):
            f.unlink()
