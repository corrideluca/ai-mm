"""Researcher — fetches and formats market data for Claude Code to analyze."""

import json
from core import client as pm, cache


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

            outcomes = m.outcomes if isinstance(m.outcomes, list) else json.loads(m.outcomes or "[]")
            prices = m.outcome_prices if isinstance(m.outcome_prices, list) else json.loads(m.outcome_prices or "[]")
            token_ids = m.token_ids if isinstance(m.token_ids, list) else json.loads(m.token_ids or "[]")

            # Get midpoints from CLOB for accuracy
            live_prices = {}
            for tid, outcome in zip(token_ids, outcomes):
                try:
                    live_prices[outcome] = pm.get_midpoint(tid)
                except Exception:
                    live_prices[outcome] = None

            markets.append({
                "question": m.question,
                "condition_id": m.condition_id,
                "outcomes": outcomes,
                "prices": prices,
                "live_prices": live_prices,
                "token_ids": token_ids,
                "volume": m.volume_num,
                "volume_24hr": getattr(m, "volume_24hr", None),
                "liquidity": m.liquidity_num,
                "end_date": m.end_date_iso,
                "description": (m.description or "")[:300],
                "event": e.title,
            })

    result = {"markets": markets, "count": len(markets)}
    cache.set("markets_scan", result)
    return result


def get_market_detail(condition_id: str) -> dict:
    """Get detailed info on a specific market via Gamma."""
    gamma = pm.get_gamma()
    markets = gamma.get_markets(condition_id=condition_id)
    if markets:
        m = markets[0] if isinstance(markets, list) else markets
        return m.model_dump()
    return {}
