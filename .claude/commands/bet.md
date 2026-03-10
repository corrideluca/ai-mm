Place a bet on Polymarket. NO CONFIRMATION NEEDED — execute directly.

Arguments: $ARGUMENTS (format: "<token_id> <amount> <side> <market_name> <reasoning>")

Steps:
1. Parse the arguments
2. Run risk check — if it fails, STOP (risk limits are the only gate)
3. Execute immediately:
```
cd /Users/corri/polymarket-agent && python3 -c "
from agents.trader import execute_trade
import json
result = execute_trade('TOKEN_ID', AMOUNT, 'SIDE', 'MARKET_NAME', 'REASONING')
print(json.dumps(result, indent=2))
"
```
4. Show the result and updated balance
5. Log reasoning to memory/strategies.md if it reveals a new pattern
