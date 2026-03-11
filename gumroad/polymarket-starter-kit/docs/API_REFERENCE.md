# API Reference

All functions available in this kit.

---

## core/client.py

### Market Data

```python
from core.client import get_events, get_midpoint, get_orderbook

# Get top active events (sorted by volume)
events = get_events(active=True, closed=False, limit=20)

# Get live price for a token (0.0 to 1.0)
price = get_midpoint("0xtoken_id_here")
# Returns: 0.75 (= 75 cents per share = 75% probability)

# Get full order book
book = get_orderbook("0xtoken_id_here")
```

### Trading

```python
from core.client import place_limit_order, place_market_order, cancel_all

# Place a limit order (GTC — good till cancelled)
result = place_limit_order(
    token_id="0x...",
    price=0.75,       # price per share in USDC
    size=10.0,        # number of shares (min 5)
    side="BUY",       # "BUY" or "SELL"
)

# Place an instant market order (FOK — fill or kill)
result = place_market_order(
    token_id="0x...",
    amount=10.0,  # USDC amount to spend
    side="BUY",
)

# Cancel everything
cancel_all()
```

### Portfolio

```python
from core.client import get_balance, get_orders, get_positions

balance = get_balance()      # float: USDC available
orders = get_orders()        # list: open limit orders
positions = get_positions()  # list: filled positions
```

---

## agents/researcher.py

```python
from agents.researcher import scan_markets, scan_overnight, get_market_detail

# Top markets by volume (good for general scanning)
data = scan_markets(limit=50)
# Returns: {"markets": [...], "count": N}

# Markets resolving in next N hours (best for short-term trades)
data = scan_overnight(hours=48)
# Automatically tries 48h, then 168h, then 504h if empty
# Returns: {"markets": [...], "count": N, "cutoff_hours": 48}

# Detailed info on a specific market
detail = get_market_detail("0xcondition_id")
```

### Market object structure

```python
{
    "question": "Will X happen by Y date?",
    "condition_id": "0x...",
    "outcomes": ["Yes", "No"],
    "live_prices": {
        "Yes": 0.75,   # 75c = 75% probability
        "No": 0.25,
    },
    "token_ids": ["0x...", "0x..."],  # use for trading
    "volume": 12500.0,               # total USDC traded
    "liquidity": 3200.0,             # available liquidity
    "end_date": "2026-03-15 00:00:00",
    "description": "Market description...",
    "event": "Oscar Awards 2026",
}
```

---

## agents/trader.py

```python
from agents.trader import execute_trade, get_portfolio

# Execute a trade with risk checks
result = execute_trade(
    token_id="0x...",
    amount=10.0,                      # USDC to spend
    side="BUY",                       # "BUY" or "SELL"
    market_name="Oscar Best Picture", # for logging
    reasoning="Swept all precursors", # for logging
    price=None,                       # fetch live if None
)

# Returns:
# {"status": "LIVE", "price": 0.75, "size": 13.3, "order_id": "...", "balance": 25.50}
# {"status": "BLOCKED", "reasons": ["Exceeds max bet"], "balance": 25.50}
# {"status": "FAILED", "error": "...", "balance": 25.50}

# Get full portfolio
portfolio = get_portfolio()
# Returns: {"balance": 25.50, "orders": [...], "positions": [...]}
```

---

## agents/risk.py

```python
from agents.risk import check_can_trade, get_daily_pnl, log_trade

# Check if a trade is allowed (called automatically by execute_trade)
result = check_can_trade(amount=10.0, balance=50.0)
# Returns: {"allowed": True, "max_bet": 10.0, "daily_pnl": -2.50, ...}

# Get today's net P&L from trade log
pnl = get_daily_pnl()
# Returns: -3.50 (= lost $3.50 today)

# Log a trade manually
log_trade({
    "market": "S&P 500 Down",
    "side": "BUY",
    "amount": 5.0,
    "price": 0.55,
    "status": "LIVE",
    "reasoning": "CPI report catalyst",
})
```

---

## core/cache.py

```python
from core.cache import get, set, clear

# Cache any value for 5 minutes
set("my_key", {"data": [1, 2, 3]})

# Retrieve (returns None if expired/missing)
data = get("my_key")

# Clear everything
clear()

# Clear specific key
clear("my_key")
```
