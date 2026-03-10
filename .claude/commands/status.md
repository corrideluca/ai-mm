Show current portfolio status on Polymarket.

```
cd /Users/corri/polymarket-agent && python -c "
from agents.trader import get_portfolio
import json
result = get_portfolio()
print(json.dumps(result, indent=2))
"
```

Display:
1. Current USDC balance
2. Open positions with current prices
3. Unrealized P&L per position
4. Total portfolio value
5. Risk status (how much room left before daily loss limit)
