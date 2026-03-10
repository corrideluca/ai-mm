Scan Polymarket for trading opportunities. PRIORITIZE SHORT-TERM markets.

Run the data fetcher:
```
cd /Users/corri/polymarket-agent && python3 -c "
from agents.researcher import scan_markets
import json
result = scan_markets(limit=30)
print(json.dumps(result, indent=2))
"
```

YOU (Claude) are the analyst. After getting the raw data:

## Priority: SHORT-TERM MARKETS (resolving within 1-7 days)
These are your bread and butter for overnight trading:
- Markets closing TONIGHT or TOMORROW get highest priority
- Markets closing within 1 week are next
- Look for near-certainties priced at 85-95¢ — small edge but high confidence
- Look for near-impossibilities priced at 5-15¢ — sell or buy the opposite side
- Time decay works in your favor on these

## Analysis steps:
1. SORT markets by end_date — nearest first
2. Filter for markets resolving within 7 days
3. Estimate fair probabilities based on your knowledge + news research
4. Compare your fair price vs market price to find edges
5. Show a clean table: Market | Closes | Market Price | Your Fair Price | Edge | Confidence
6. Recommend specific trades with reasoning
7. For longer-dated markets, only flag if edge > 15%

## After analysis:
- Update memory/markets.md with findings
- Update memory/strategies.md if you learn something new

If you're unsure about a market, use WebSearch to research recent news before betting.

Be honest about your uncertainty. Only recommend bets where you have genuine conviction.
