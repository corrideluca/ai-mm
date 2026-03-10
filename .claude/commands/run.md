Full autonomous trading cycle. ALWAYS BET — never skip a cycle without placing trades.

Steps:
1. Clear cache for fresh data:
```
cd /Users/corri/polymarket-agent && python3 -c "from core.cache import clear; clear()"
```

2. Check current portfolio + balance:
```
cd /Users/corri/polymarket-agent && python3 -c "
from agents.trader import get_portfolio
import json
print(json.dumps(get_portfolio(), indent=2))
"
```

3. Fetch markets — start tight, widen until you find something:
```
cd /Users/corri/polymarket-agent && python3 -c "
from agents.researcher import scan_overnight
import json
for hours in [48, 168, 504]:
    result = scan_overnight(hours=hours)
    if result['count'] > 0:
        print(json.dumps(result, indent=2))
        break
    print(f'{hours}h: 0 markets, widening...')
else:
    from agents.researcher import scan_markets
    print(json.dumps(scan_markets(limit=30), indent=2))
"
```

4. YOU (Claude) analyze — ALWAYS FIND A BET:
   - **PRIORITY 1**: Markets resolving TONIGHT or TOMORROW (< 48h)
   - **PRIORITY 2**: Markets resolving this week (48h-168h) — Oscars, sports, S&P daily, crypto prices
   - **PRIORITY 3**: If nothing short-term, bet the best edge you can find at ANY timeframe
   - **NEVER return empty-handed** — if you have balance, find the best available bet and take it
   - Use WebSearch to research any market before betting — check scores, results, predictions, odds
   - Look for: S&P/crypto daily close markets, sports results, awards shows, scheduled events
   - Near-certainties (>90%) and near-impossibilities (<10%) are your bread and butter
   - Check memory/performance.md and memory/strategies.md before betting

5. DEPLOY CAPITAL — spread bets across multiple markets:
   - Split available balance across your best 2-5 opportunities
   - Don't put everything on one bet — diversify across markets
   - Respect risk limits (max 20% per bet, 50% per market) but otherwise GO ALL IN
   - If a previous bet resolved and freed up cash, re-deploy it immediately

6. For each trade, execute directly:
```
cd /Users/corri/polymarket-agent && python3 -c "
from agents.trader import execute_trade
import json
result = execute_trade('TOKEN_ID', AMOUNT, 'SIDE', 'MARKET_NAME', 'REASONING')
print(json.dumps(result, indent=2))
"
```

7. After all trades, update:
   - memory/performance.md (automatic via risk.py)
   - memory/strategies.md (manual — write what you learned)
   - memory/markets.md (manual — note markets to watch for next cycle)

8. Show a summary: trades made, current positions, balance, next actions.

9. If using /loop — on each cycle, check if any positions resolved and calculate realized P&L. Re-deploy freed capital.
