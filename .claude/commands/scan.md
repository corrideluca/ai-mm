Scan Polymarket for OVERNIGHT trading opportunities. Only care about markets resolving in HOURS or by tomorrow.

Run the overnight data fetcher:
```
cd /Users/corri/polymarket-agent && python3 -c "
from agents.researcher import scan_overnight
import json
result = scan_overnight(hours=48)
print(json.dumps(result, indent=2))
"
```
If empty, widen to 72h:
```
cd /Users/corri/polymarket-agent && python3 -c "
from agents.researcher import scan_overnight
import json
result = scan_overnight(hours=72)
print(json.dumps(result, indent=2))
"
```

YOU (Claude) are the analyst. After getting the raw data:

## Priority: OVERNIGHT MARKETS ONLY (resolving within 48 hours)
- Markets closing TONIGHT or TOMORROW — this is ALL you care about
- Skip anything resolving more than 2-3 days out
- Look for events that already happened (scores, results, announcements) where market hasn't settled
- Look for near-certainties priced at 85-95¢ — guaranteed money overnight
- Look for near-impossibilities priced at 5-15¢ — free money on the other side
- Sports, daily events, deadlines passing tonight = your bread and butter

## Analysis steps:
1. SORT markets by end_date — nearest first
2. FILTER OUT anything resolving more than 48 hours from now
3. Use WebSearch to check if the event already happened / latest results
4. Compare your fair price vs market price to find edges
5. Show a clean table: Market | Closes | Market Price | Your Fair Price | Edge | Confidence
6. Recommend specific trades with reasoning
7. IGNORE longer-dated markets completely unless edge > 20%

## After analysis:
- Update memory/markets.md with findings
- Update memory/strategies.md if you learn something new

If you're unsure about a market, use WebSearch to research recent news before betting.

Be honest about your uncertainty. Only recommend bets where you have genuine conviction.
