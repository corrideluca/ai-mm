5-min crypto trading with TECHNICAL ANALYSIS. Never bet blind.

## Non-stop trading (default: 100 rounds, ~8 hours)
```
source .venv/Scripts/activate && PYTHONPATH=. PYTHONIOENCODING=utf-8 python agents/crypto_trader.py 100
```

## Quick 3-round session (~15 min)
```
source .venv/Scripts/activate && PYTHONPATH=. PYTHONIOENCODING=utf-8 python agents/crypto_trader.py 3
```

## How it works
Each round:
1. Waits until 90s into the 5-min window (let price action develop)
2. Fetches 15 1-min candles from Binance for BTC, ETH, SOL, XRP
3. Calculates: momentum (5m + 15m), EMA crossover, RSI, volume spike, candle pattern
4. Only bets when score >= 3 (STRONG signal). Skips weak/neutral = no bet
5. High confidence (score>=4): 15% of balance @ 52c. Medium: 10% @ 48c
6. Tracks wins/losses and running P&L per session

## CRITICAL RULES
- **NEVER bet blind** — lost $30 -> $7 in 3 rounds with blind betting
- Min score = 3 to trade (skip neutral/weak signals)
- Max 20% of balance per coin per window
- Patience = profit. Skipping a window costs $0. Bad bets cost everything.

## Analysis only (no trades)
```
source .venv/Scripts/activate && PYTHONPATH=. PYTHONIOENCODING=utf-8 python agents/crypto_analyzer.py
```

## After trading
- Log results to memory/performance.md
- Update strategies.md with indicator learnings
