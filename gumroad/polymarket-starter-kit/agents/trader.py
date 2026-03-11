"""Trader — executes trades after passing risk checks.

Usage:
    from agents.trader import execute_trade, get_portfolio

    result = execute_trade(
        token_id="0x...",
        amount=10.00,
        side="BUY",
        market_name="Will X win the Oscar?",
        reasoning="Won all major precursors, edge ~10c",
    )
    print(result)
"""

from core import client as pm
from agents.risk import check_can_trade, log_trade


def execute_trade(
    token_id: str,
    amount: float,
    side: str = "BUY",
    market_name: str = "",
    reasoning: str = "",
    price: float = None,
) -> dict:
    """Execute a trade with automatic risk checking.

    The trade is blocked if it exceeds any risk limit.
    No confirmation required — set your limits in .env and trust the system.

    Args:
        token_id: The outcome token ID (from researcher.py market data)
        amount: Dollar amount in USDC (e.g., 10.0 = $10)
        side: "BUY" to bet Yes/No, "SELL" to exit a position
        market_name: Human-readable name for logging
        reasoning: Why you're making this bet (logged for review)
        price: Override price (fetches live price if None)

    Returns:
        dict with status, price, order_id, balance
    """
    balance = pm.get_balance()

    # Check risk limits first
    risk = check_can_trade(amount, balance)
    if not risk["allowed"]:
        return {
            "status": "BLOCKED",
            "reasons": risk["reasons"],
            "balance": balance,
        }

    # Fetch live price if not provided
    if price is None:
        try:
            price = pm.get_midpoint(token_id)
        except Exception:
            price = 0.0

    try:
        # Convert USDC amount to shares (min 5 shares per Polymarket rules)
        size = max(amount / price, 5.0) if price > 0 else 5.0

        result = pm.place_limit_order(
            token_id=token_id,
            price=price,
            size=size,
            side=side,
        )

        status = "LIVE" if (result and result.success) else "FAILED"

        trade = {
            "market": market_name,
            "side": side,
            "amount": amount,
            "price": price,
            "size": size,
            "status": status,
            "order_id": getattr(result, "order_id", None),
            "reasoning": reasoning,
        }
        log_trade(trade)

        return {
            "status": status,
            "price": price,
            "amount": amount,
            "size": size,
            "side": side,
            "market": market_name,
            "order_id": getattr(result, "order_id", None),
            "balance": balance,
        }

    except Exception as e:
        log_trade({
            "market": market_name,
            "side": side,
            "amount": amount,
            "price": price,
            "status": f"FAILED: {e}",
            "reasoning": reasoning,
        })
        return {"status": "FAILED", "error": str(e), "balance": balance}


def get_portfolio() -> dict:
    """Get current portfolio: balance, open orders, and positions."""
    return {
        "balance": pm.get_balance(),
        "orders": pm.get_orders(),
        "positions": pm.get_positions(),
    }
