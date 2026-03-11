"""Polymarket API client — wraps polymarket-apis for easy use.

Uses:
- CLOB (Central Limit Order Book) for trading
- Gamma for rich market data

Auth uses signature_type=1 (poly proxy wallet) — works with MetaMask keys.
"""

from polymarket_apis import PolymarketClobClient, PolymarketGammaClient
from polymarket_apis.types.clob_types import OrderArgs, MarketOrderArgs
from core.config import config

_clob = None
_gamma = None


def get_clob() -> PolymarketClobClient:
    """Get authenticated CLOB client (cached singleton)."""
    global _clob
    if _clob is None:
        _clob = PolymarketClobClient(
            private_key=config.private_key,
            address=config.funder_address,
            chain_id=config.chain_id,
            signature_type=1,  # poly proxy wallet
        )
    return _clob


def get_gamma() -> PolymarketGammaClient:
    """Get Gamma client for market data (no auth needed)."""
    global _gamma
    if _gamma is None:
        _gamma = PolymarketGammaClient()
    return _gamma


# === Market Data ===

def get_events(active=True, closed=False, limit=20):
    """Get events with full market data via Gamma."""
    return get_gamma().get_events(active=active, closed=closed, limit=limit)


def get_midpoint(token_id: str) -> float:
    """Get current midpoint price for a token (0.0 to 1.0)."""
    mid = get_clob().get_midpoint(token_id)
    return float(mid.value) if hasattr(mid, "value") else float(mid)


def get_orderbook(token_id: str):
    """Get full order book for a token."""
    return get_clob().get_order_book(token_id)


# === Trading ===

def place_limit_order(token_id: str, price: float, size: float, side: str = "BUY"):
    """Place a GTC limit order. Min size is 5 shares.

    Args:
        token_id: The outcome token ID from the market data
        price: Price per share (0.0 to 1.0, e.g. 0.75 = 75c)
        size: Number of shares (min 5)
        side: "BUY" or "SELL"
    """
    return get_clob().create_and_post_order(
        OrderArgs(
            token_id=token_id,
            price=price,
            size=max(size, 5.0),  # enforce Polymarket minimum
            side=side,
        )
    )


def place_market_order(token_id: str, amount: float, side: str = "BUY"):
    """Place an instant market order (FOK — fill or kill).

    Args:
        token_id: The outcome token ID
        amount: Dollar amount in USDC
        side: "BUY" or "SELL"
    """
    return get_clob().create_and_post_market_order(
        MarketOrderArgs(
            token_id=token_id,
            amount=amount,
            side=side,
        )
    )


def cancel_order(order_id: str):
    """Cancel a specific open order."""
    return get_clob().cancel_order(order_id)


def cancel_all():
    """Cancel all open orders."""
    return get_clob().cancel_all()


# === Portfolio ===

def get_balance() -> float:
    """Get available USDC balance."""
    return get_clob().get_usdc_balance()


def get_orders():
    """Get all open orders."""
    return get_clob().get_orders()


def get_positions():
    """Get current positions (filled bets waiting to resolve)."""
    try:
        return get_clob().get_token_balance()
    except Exception:
        return []
