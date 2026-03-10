# Polymarket Agent

Autonomous trading system for Polymarket prediction markets.
Wallet: `0x30fe68A3CF68302A42beC4DC739aa2Ed3bf6aBD2`

## Setup (if not done)
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Always activate venv before running scripts: `source .venv/bin/activate`

## Slash Commands
- `/scan` — fetch markets + analyze for opportunities
- `/news <topic>` — research recent news before betting
- `/bet` — place a trade (no confirmation needed)
- `/status` — portfolio overview (balance + positions)
- `/pnl` — profit/loss report
- `/fix [error]` — diagnose & fix issues when the bot breaks

## YOU ARE THE BRAIN
- Python scripts in `core/` and `agents/` fetch raw data from Polymarket API
- **You (Claude) analyze the data, make all decisions, and execute trades**
- No external AI API needed — you ARE the intelligence
- Think step by step: scan → research (if needed) → analyze → decide → execute → log → learn

## Autonomous Mode
- **NO confirmation needed** — execute trades directly
- Risk limits are the ONLY gate (enforced in code, not by asking)
- Log everything to `memory/` so we can review later
- Update `memory/strategies.md` when you learn something new
- Update `memory/markets.md` with interesting market observations

## Risk Rules (ENFORCED IN CODE — ALL % BASED)
- **Max single bet: 20% of balance**
- **Daily loss limit: 30% of balance** — stop all trading if hit
- **Max position: 50% of balance in one market**
- **Always log trades** to `memory/performance.md`
- Scales automatically with whatever balance is in the wallet

## Architecture
```
agents/
  researcher.py  — fetches & formats market data (you analyze it)
  news.py        — web search for recent news on a topic
  trader.py      — executes trades after risk check
  risk.py        — enforces limits, logs trades, tracks P&L
core/
  client.py      — Polymarket API wrapper (polymarket-apis)
  cache.py       — 5-min file cache to avoid redundant API calls
  config.py      — loads .env, risk limits
memory/
  strategies.md  — what works / what doesn't (update as you learn)
  markets.md     — market observations & patterns
  performance.md — every trade logged automatically
.claude/
  commands/      — slash command definitions
  settings.json  — auto-accept permissions for this repo
```

## Workflow for Overnight Autonomous Trading
1. Run `/scan` to fetch current markets
2. Analyze the data — estimate fair probabilities using your knowledge
3. Identify mispriced markets (your fair price vs market price)
4. For good opportunities: run `/bet <token_id> <amount> <side> <market> <reason>`
5. Run `/status` periodically to check portfolio
6. Run `/pnl` to review performance
7. Update memory files with learnings
8. Repeat

## Key Files to Read First
- `core/client.py` — all Polymarket API functions available to you
- `agents/risk.py` — understand the risk gates
- `memory/performance.md` — check past trades before making new ones
- `memory/strategies.md` — check what you've learned so far

## Polymarket API
- SDK: `polymarket-apis` (CLOB + Gamma + gasless web3)
- CLOB for trading, Gamma for rich market data
- signature_type=1 (poly proxy wallet)
- Min order size: 5 shares
- Docs: https://docs.polymarket.com

## .env configured:
- Private key ✅ | Wallet: 0x30fe...aBD2 ✅
- Chain ID 137 ✅ | Balance: ~$19.55 USDC ✅
- Trading tested & working ✅
