Clear the market data cache to force fresh data on next scan.

```
cd /Users/corri/polymarket-agent && python3 -c "
from core.cache import clear
clear()
print('Cache cleared.')
"
```
