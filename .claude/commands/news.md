Research news about a topic before placing bets.

Usage: /news <topic or market question>

Arguments: $ARGUMENTS

Steps:
1. Search the web for recent news about: $ARGUMENTS
2. Use WebSearch to find 3-5 recent, relevant articles
3. Summarize the key facts that could affect the outcome
4. Assess how the news shifts probabilities (bullish/bearish on each outcome)
5. Cache the research so we don't repeat it:
```
cd /Users/corri/polymarket-agent && python3 -c "
from agents.news import cache_research
cache_research('$ARGUMENTS', '''YOUR_SUMMARY_HERE''')
"
```

Focus on:
- **Recency** — what happened in the last 24-72 hours?
- **Source quality** — prefer major outlets, official statements, data releases
- **Market impact** — how does this change the probability of the outcome?
- **Consensus vs contrarian** — is the market already pricing this in?

After research, give a clear verdict:
- Does the news support a trade? If so, which side and why?
- What's the confidence level? (low/medium/high)
- Any upcoming events that could change things?
