"""Trader agent — executes trades autonomously after risk check."""

from core import client as pm
from agents.risk import check_can_trade, log_trade


def execute_trade(token_id: str, amount: float, side: str = "BUY", market_name: str = "", reasoning: str = "", price: float = None) -> dict:
    """Execute a trade if risk checks pass. No confirmation needed."""

    balance = pm.get_balance()

    # Risk check
    risk_check = check_can_trade(amount, balance)
    if not risk_check["allowed"]:
        return {
            "status": "BLOCKED",
            "reasons": risk_check["reasons"],
            "balance": balance,
        }

    # Get current price if not provided
    if price is None:
        try:
            price = pm.get_midpoint(token_id)
        except Exception:
            price = 0.0

    try:
        # Use limit order at current price for better fills
        size = amount / price if price > 0 else amount
        size = max(size, 5.0)  # minimum 5 shares

        result = pm.place_limit_order(
            token_id=token_id,
            price=price,
            size=size,
            side=side,
        )

        status = "LIVE" if (result and result.success) else "FAILED"
        order_id = result.order_id if result else None

        trade = {
            "market": market_name,
            "side": side,
            "amount": amount,
            "price": price,
            "size": size,
            "status": status,
            "order_id": order_id,
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
            "order_id": order_id,
            "balance": balance,
        }

    except Exception as e:
        trade = {
            "market": market_name,
            "side": side,
            "amount": amount,
            "price": price,
            "status": f"FAILED: {e}",
            "reasoning": reasoning,
        }
        log_trade(trade)

        return {
            "status": "FAILED",
            "error": str(e),
            "balance": balance,
        }


def get_portfolio() -> dict:
    """Get current positions and balance."""
    return {
        "balance": pm.get_balance(),
        "orders": pm.get_orders(),
        "positions": pm.get_positions(),
    }
