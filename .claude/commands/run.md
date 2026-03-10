Full autonomous trading cycle. FOCUS ON OVERNIGHT markets — ones resolving in HOURS or by tomorrow.

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

3. Fetch OVERNIGHT markets (resolving within 48h):
```
cd /Users/corri/polymarket-agent && python3 -c "
from agents.researcher import scan_overnight
import json
print(json.dumps(scan_overnight(hours=48), indent=2))
"
```
If no overnight markets found, widen to 72h:
```
cd /Users/corri/polymarket-agent && python3 -c "
from agents.researcher import scan_overnight
import json
print(json.dumps(scan_overnight(hours=72), indent=2))
"
```

4. YOU (Claude) analyze — OVERNIGHT PRIORITY:
   - **ONLY CARE ABOUT**: Markets resolving TONIGHT, TOMORROW, or within 48 hours
   - **MAYBE**: Markets resolving in 2-3 days if edge is huge (>20%)
   - **SKIP EVERYTHING ELSE** — do NOT trade markets weeks/months out
   - Check memory/performance.md for past trades
   - Check memory/strategies.md for what worked before
   - Use WebSearch to check latest news/scores/results for any market you're considering
   - Look for near-certainties or near-impossibilities — events that are basically decided already
   - Sports scores, election results, events that already happened but market hasn't settled yet

5. For any trade you want to make, execute it directly:
```
cd /Users/corri/polymarket-agent && python3 -c "
from agents.trader import execute_trade
import json
result = execute_trade('TOKEN_ID', AMOUNT, 'SIDE', 'MARKET_NAME', 'REASONING')
print(json.dumps(result, indent=2))
"
```

6. After all trades, update:
   - memory/performance.md (automatic via risk.py)
   - memory/strategies.md (manual — write what you learned)
   - memory/markets.md (manual — note markets to watch for next cycle)

7. Show a summary: trades made, current positions, balance, next actions.

8. If using /loop — on each cycle, check if any positions resolved and calculate realized P&L.
