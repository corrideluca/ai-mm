"""Researcher — fetches and formats Polymarket data for AI analysis.

Usage:
    from agents.researcher import scan_overnight, scan_markets
    import json

    # Get markets resolving in next 48 hours
    data = scan_overnight(hours=48)
    print(json.dumps(data, indent=2))
    # Feed this to Claude/GPT for analysis
"""

import json
from datetime import datetime, timedelta
from core import client as pm, cache


def _parse_end_date(m):
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
    """Convert a market object to a clean dict."""
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
        "live_prices": live_prices,    # current market prices (0.0-1.0)
        "token_ids": token_ids,        # use these for trading
        "volume": m.volume_num,        # total volume in USDC
        "liquidity": m.liquidity_num,  # available liquidity
        "end_date": str(end) if end else None,
        "description": (m.description or "")[:300],
        "event": e.title,
    }


def scan_markets(limit: int = 20) -> dict:
    """Fetch top active markets by volume.

    Returns:
        {"markets": [...], "count": N}
    """
    cached = cache.get("markets_scan")
    if cached:
        return cached

    events = pm.get_events(active=True, closed=False, limit=limit)
    markets = []
    for e in events:
        for m in e.markets:
            if m.active:
                markets.append(_market_to_dict(m, e))

    result = {"markets": markets, "count": len(markets)}
    cache.set("markets_scan", result)
    return result


def scan_overnight(hours: int = 48) -> dict:
    """Fetch markets resolving within the next N hours.

    Best for finding short-term trading opportunities (daily S&P, sports, etc.)
    Sorted soonest-first. Fetches 500 events to catch all short-term markets.

    Args:
        hours: Look ahead window (48 = 2 days, 168 = 1 week)

    Returns:
        {"markets": [...], "count": N, "cutoff_hours": hours}
    """
    cache_key = f"overnight_{hours}h"
    cached = cache.get(cache_key)
    if cached:
        return cached

    now = datetime.utcnow()
    cutoff = now + timedelta(hours=hours)

    events = pm.get_events(active=True, closed=False, limit=500)
    markets = []

    for e in events:
        for m in e.markets:
            if not m.active:
                continue
            end = _parse_end_date(m)
            if end and now < end <= cutoff:
                markets.append(_market_to_dict(m, e))

    markets.sort(key=lambda x: x["end_date"] or "9999")
    result = {"markets": markets, "count": len(markets), "cutoff_hours": hours}
    cache.set(cache_key, result)
    return result


def get_market_detail(condition_id: str) -> dict:
    """Get detailed info on a specific market by condition ID."""
    gamma = pm.get_gamma()
    markets = gamma.get_markets(condition_id=condition_id)
    if markets:
        m = markets[0] if isinstance(markets, list) else markets
        return m.model_dump()
    return {}
