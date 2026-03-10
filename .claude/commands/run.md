Full autonomous trading cycle. FOCUS ON SHORT-TERM markets that resolve soon.

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

3. Fetch markets (get more to find short-term ones):
```
cd /Users/corri/polymarket-agent && python3 -c "
from agents.researcher import scan_markets
import json
print(json.dumps(scan_markets(limit=50), indent=2))
"
```

4. YOU (Claude) analyze — PRIORITIZE BY URGENCY:
   - **FIRST**: Markets resolving in < 24 hours (tonight/tomorrow)
   - **SECOND**: Markets resolving in 1-3 days
   - **THIRD**: Markets resolving in 3-7 days
   - **LAST**: Longer-dated only if edge > 15%
   - Check memory/performance.md for past trades
   - Check memory/strategies.md for what worked before
   - For markets you're unsure about, use WebSearch to research recent news
   - Look for near-certainties or near-impossibilities — these are your edge overnight

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
