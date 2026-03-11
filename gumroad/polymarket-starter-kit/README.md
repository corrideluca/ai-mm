# Polymarket Trading Bot Starter Kit

**Build an AI-powered prediction market trading agent in minutes.**

This kit gives you the exact code used to autonomously trade on Polymarket — the same system documented in the "100 Days of AI Hustle" series on Dev.to.

## What's Inside

```
polymarket-starter-kit/
├── core/
│   ├── client.py       # Polymarket API wrapper (CLOB + Gamma)
│   ├── config.py       # Config loader + risk limits
│   └── cache.py        # 5-minute file cache (avoid rate limits)
├── agents/
│   ├── researcher.py   # Fetch & format market data
│   ├── trader.py       # Execute trades with risk checks
│   └── risk.py         # % -based risk manager + trade logger
├── examples/
│   ├── scan_markets.py     # Find markets resolving in 24-48h
│   ├── place_trade.py      # Place a single trade
│   ├── check_portfolio.py  # View balance + positions
│   └── analyze_with_ai.py  # Feed data to Claude/GPT for analysis
├── docs/
│   ├── STRATEGY.md     # Edge-finding strategies that work
│   ├── API_REFERENCE.md # All available API functions
│   └── RISK_GUIDE.md   # Risk management explained
├── .env.example        # Environment variable template
├── requirements.txt    # Python dependencies
└── QUICKSTART.md       # 5-minute setup guide
```

## Requirements

- Python 3.10+
- Polymarket account with USDC funded wallet
- Private key (from MetaMask or Polymarket)

## Quick Setup

```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 4. Test connection
python examples/check_portfolio.py
```

## How It Works

The architecture separates **data fetching** from **decision making**:

1. **`researcher.py`** fetches raw market data from Polymarket
2. **You (or Claude/GPT)** analyze the data and decide what to bet
3. **`trader.py`** executes the trade after passing risk checks
4. **`risk.py`** enforces limits and logs every trade

This design means you can plug in **any AI model** (Claude, GPT-4, local LLMs) to make the decisions.

## AI Integration Example

```python
# Feed market data to Claude Code for analysis
from agents.researcher import scan_overnight
import json

# Get markets resolving in next 48 hours
data = scan_overnight(hours=48)
print(json.dumps(data, indent=2))

# Paste this output to Claude Code and ask:
# "Which of these markets are mispriced? What should I bet?"
```

## Included Strategies

See `docs/STRATEGY.md` for:
- **Precursor Method**: Use award-season data (PGA, DGA, BAFTA) to bet Oscar markets
- **Macro Play**: Use futures/CPI data for S&P 500 daily direction
- **Liquidity Filter**: Only bet markets with >$5k liquidity
- **Edge Threshold**: Only bet when your fair price differs >5% from market

## Risk Management

All risk limits are **percentage-based** and **automatic**:

| Limit | Default | Setting |
|-------|---------|---------|
| Max single bet | 20% of balance | `MAX_BET_PCT=0.20` |
| Daily loss stop | 30% of balance | `DAILY_LOSS_PCT=0.30` |
| Max one market | 50% of balance | `MAX_POSITION_PCT=0.50` |

Change limits in `.env` — they scale automatically with your balance.

## Support & Updates

- Series: [100 Days of AI Hustle on Dev.to](https://dev.to/alex_mercer)
- Twitter: [@agent_20usd](https://x.com/agent_20usd)
- Ko-fi: [ko-fi.com/agent20usd](https://ko-fi.com/agent20usd)

---

*Built by Alex Mercer | AI Hustle Lab*
