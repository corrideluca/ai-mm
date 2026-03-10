# Polymarket Trader — Claude Code Skill

An autonomous prediction market trading skill for Claude Code. This skill teaches Claude how to analyze Polymarket prediction markets, estimate fair probabilities, identify mispriced opportunities, and execute trades with built-in risk management.

## What It Does

- **Scans** active Polymarket markets via the Gamma API, prioritizing short-dated opportunities
- **Analyzes** each market by estimating fair probabilities using reasoning, base rates, and web research
- **Identifies edges** by comparing fair prices to market prices (minimum 5-cent threshold)
- **Executes trades** autonomously via the Polymarket CLOB API on Polygon (USDC on chain ID 137)
- **Enforces risk limits** — max 20% per trade, 50% per market, 30% daily loss limit (all percentage-based)
- **Logs everything** — every trade is recorded with reasoning for performance review
- **Learns over time** — updates strategy notes and market observations after each cycle

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Agent20/polymarket-trader-skill.git
cd polymarket-trader-skill
```

### 2. Set Up Python Environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Dependencies:
- `polymarket-apis>=0.5.0` — Polymarket SDK (CLOB + Gamma + gasless web3)
- `python-dotenv>=1.0.0` — environment variable loading
- `rich>=13.0.0` — terminal formatting

### 3. Configure Credentials

Create a `.env` file in the project root:

```env
POLYMARKET_PRIVATE_KEY=0xYOUR_POLYGON_PRIVATE_KEY
POLYMARKET_FUNDER_ADDRESS=0xYOUR_WALLET_ADDRESS
POLYMARKET_API_KEY=your_clob_api_key
POLYMARKET_API_SECRET=your_clob_api_secret
POLYMARKET_API_PASSPHRASE=your_clob_api_passphrase
CHAIN_ID=137
```

To derive CLOB API credentials from your private key:

```python
from polymarket_apis import PolymarketClobClient
client = PolymarketClobClient(private_key="0xYOUR_KEY", chain_id=137, signature_type=1)
creds = client.derive_api_key()
print(creds)  # {"apiKey": "...", "secret": "...", "passphrase": "..."}
```

### 4. Fund Your Wallet

Transfer USDC to your wallet on Polygon (chain ID 137). The bot needs USDC to place trades. Risk limits are percentage-based, so it works with any balance.

### 5. Add the Skill to Claude Code

Copy `SKILL.md` into your Claude Code skills directory, or reference it from your project's `.claude/commands/` folder.

## Usage

Once installed, Claude Code can run the full trading workflow through slash commands:

### Scan for Opportunities
```
/scan
```
Fetches markets resolving within 48 hours and analyzes them for edges.

### Research a Topic
```
/news <topic>
```
Searches the web for recent news relevant to a market before betting.

### Place a Trade
```
/bet <token_id> <amount> <side> <market_name> <reasoning>
```
Executes a trade directly after risk checks pass. No confirmation needed.

### Check Portfolio
```
/status
```
Shows current balance, open orders, and positions.

### View Performance
```
/pnl
```
Displays the trade log with profit/loss calculations.

### Full Autonomous Cycle
```
/run
```
Executes the complete workflow: clear cache, check portfolio, scan markets, analyze, research, trade, log, and learn.

## Architecture

```
agents/
  researcher.py  — Fetches market data from Gamma API, formats for analysis
  news.py        — Structures web search queries, caches research results
  trader.py      — Executes trades after risk check, logs to performance file
  risk.py        — Enforces percentage-based limits, calculates daily P&L
core/
  client.py      — Polymarket API wrapper (CLOB for trading, Gamma for data)
  cache.py       — 5-minute file cache to avoid redundant API calls
  config.py      — Loads .env, defines risk limit configuration
memory/
  strategies.md  — Validated trading strategies and anti-patterns
  markets.md     — Market observations, patterns, and watchlist
  performance.md — Complete trade log with date, market, side, amount, price, status, reasoning
```

## Trading Strategies

The skill comes with battle-tested strategies:

1. **Calendar Arbitrage** — When a catalyst event occurs after a market's resolution date, the "No" side is underpriced
2. **Precursor Stacking** — When a candidate sweeps all precursor signals (awards, polls), the final market underprices them
3. **News Lag** — Markets take hours to price in breaking news; early detection creates a window
4. **Near-Lock Picks** — Buying 95c+ positions for near-certain outcomes; small but safe returns
5. **Daily Market Exploitation** — S&P, crypto, and sports same-day markets where real-time data gives you an edge

## Risk Management

All limits are percentage-based and scale with your balance:

| Rule | Limit | Purpose |
|------|-------|---------|
| Max single bet | 20% of balance | Prevents overconcentration on one trade |
| Max position per market | 50% of balance | Forces diversification across markets |
| Daily loss limit | 30% of balance | Circuit breaker to prevent catastrophic loss |

These limits are enforced in code. The risk check runs before every trade and blocks execution if any limit would be violated. They are the only gate on autonomous trading.

## API Reference

The skill uses the `polymarket-apis` Python SDK:

- **Gamma API** (unauthenticated) — Market data, events, outcomes, prices, volumes
  - `GET https://gamma-api.polymarket.com/events?active=true`
- **CLOB API** (authenticated) — Order placement, portfolio, balances
  - Limit orders (GTC) and market orders (FOK)
  - Minimum order: 5 shares
  - `signature_type=1` (poly proxy wallet)

Full API docs: https://docs.polymarket.com

## Memory System

The skill maintains persistent memory across trading sessions:

- **performance.md** — Automatic trade log. Every trade is appended with date, market, side, amount, price, status, and reasoning.
- **strategies.md** — Manual strategy notes. Updated when new patterns are discovered or when a strategy fails.
- **markets.md** — Market observations. Notes on interesting markets, term structures, and items to watch for the next cycle.

## License

MIT

## Disclaimer

This is experimental software for educational purposes. Prediction market trading involves financial risk. Never trade with money you cannot afford to lose. Past performance does not guarantee future results. The authors are not responsible for any financial losses.
