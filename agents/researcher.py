"""Researcher — fetches and formats market data for Claude Code to analyze."""

import json
from datetime import datetime, timedelta
from core import client as pm, cache


def _parse_end_date(m):
    """Extract and parse end_date from a market object."""
    end = m.end_date_iso or m.end_date
    if not end:
        return None
    if isinstance(end, str):
        try:
            return datetime.fromisoformat(end.replace("Z", "+00:00").replace("+00:00", ""))
        except ValueError:
            return None
    return end


def _market_to_dict(m, e, fetch_live=True):
    """Convert a market object to a dict for Claude to analyze."""
    outcomes = m.outcomes if isinstance(m.outcomes, list) else json.loads(m.outcomes or "[]")
    prices = m.outcome_prices if isinstance(m.outcome_prices, list) else json.loads(m.outcome_prices or "[]")
    token_ids = m.token_ids if isinstance(m.token_ids, list) else json.loads(m.token_ids or "[]")

    live_prices = {}
    if fetch_live:
        for tid, outcome in zip(token_ids, outcomes):
            try:
                live_prices[outcome] = pm.get_midpoint(tid)
            except Exception:
                live_prices[outcome] = None
    else:
        for price, outcome in zip(prices, outcomes):
            live_prices[outcome] = float(price) if price else None

    end = _parse_end_date(m)
    return {
        "question": m.question,
        "condition_id": m.condition_id,
        "outcomes": outcomes,
        "prices": prices,
        "live_prices": live_prices,
        "token_ids": token_ids,
        "volume": m.volume_num,
        "volume_24hr": getattr(m, "volume_24hr", None),
        "liquidity": m.liquidity_num,
        "end_date": str(end) if end else None,
        "description": (m.description or "")[:300],
        "event": e.title,
    }


def scan_markets(limit: int = 20) -> dict:
    """Fetch active events with market data. Returns structured JSON for Claude to analyze."""
    cached = cache.get("markets_scan")
    if cached:
        return cached

    events = pm.get_events(active=True, closed=False, limit=limit)
    markets = []
    for e in events:
        for m in e.markets:
            if not m.active:
                continue
            markets.append(_market_to_dict(m, e))

    result = {"markets": markets, "count": len(markets)}
    cache.set("markets_scan", result)
    return result


def scan_overnight(hours: int = 48) -> dict:
    """Fetch markets resolving within the next N hours. Sorted by end_date (soonest first).

    Progressively widens search: tries 48h, then 168h (7 days) if empty.
    Fetches 500 events to catch daily/sports/crypto markets beyond top volume.
    """
    cache_key = f"overnight_{hours}h"
    cached = cache.get(cache_key)
    if cached:
        return cached

    now = datetime.utcnow()
    cutoff = now + timedelta(hours=hours)

    # Fetch 500 events to find daily/short-term markets (S&P, crypto, sports, Oscars, etc.)
    events = pm.get_events(active=True, closed=False, limit=500)

    markets = []
    for e in events:
        for m in e.markets:
            if not m.active:
                continue

            end = _parse_end_date(m)
            if not end or end < now or end > cutoff:
                continue

            markets.append(_market_to_dict(m, e))

    # Sort by end_date soonest first
    markets.sort(key=lambda x: x["end_date"] or "9999")

    result = {"markets": markets, "count": len(markets), "cutoff_hours": hours}
    cache.set(cache_key, result)
    return result


def get_market_detail(condition_id: str) -> dict:
    """Get detailed info on a specific market via Gamma."""
    gamma = pm.get_gamma()
    markets = gamma.get_markets(condition_id=condition_id)
    if markets:
        m = markets[0] if isinstance(markets, list) else markets
        return m.model_dump()
    return {}
