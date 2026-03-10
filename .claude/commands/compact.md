Compact the conversation to save tokens. Run this between task cycles.

Steps:
1. Before compacting, save ALL current progress to memory files:
   - memory/daily/day-NNN.md — today's full activity log
   - memory/content.md — any new content/tools/articles/tweets
   - memory/strategies.md — any new learnings
   - memory/performance.md — any new trades
   - memory/markets.md — any market observations
2. Double-check nothing is lost — re-read your memory files briefly
3. Run /compact to free context
4. After compaction, read memory files to restore context

IMPORTANT: Always save progress BEFORE compacting. Anything not in memory/ files will be lost.

Token management rules:
- Run /compact after every major task cycle (after finishing a tool, finishing trades, finishing content)
- Don't re-read files unnecessarily — check memory/ first
- Keep responses concise
- Avoid redundant API calls — use cache when possible
- When conversation gets long (50+ messages), compact proactively

Tweet rate limit reminder: Only 1 tweet per hour. Check last tweet time in memory/content.md.
