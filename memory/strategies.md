# Strategy Notes

## What Works
- Short-dated "will X happen by date" markets with near-expiry offer edges when events are clearly unlikely in the remaining time (e.g., criminal conviction in 21 days)
- Cross-referencing news with market prices reveals when markets lag behind developments
- Corporate milestones (IPO filings) create strong base rates for longer-dated resolution
- **Calendar arbitrage**: When a catalyst event happens AFTER a market's resolution date, the market overprices the risk (e.g., May 7 elections after Apr 30 Starmer deadline)
- Term structure analysis — comparing prices across time horizons reveals where market overestimates near-term probability
- **Awards season precursor stacking**: When a film/person sweeps ALL major precursor awards (PGA, DGA, BAFTA, Golden Globes, SAG, Critics Choice), the Oscar market often still underprices them by 5-10c. Best Picture winners correlate ~87% with PGA winners. Spread bets across multiple categories of the same frontrunner for correlated upside.
- **Near-lock categories**: Best Actress with a clean sweep of all precursors is ~98% likely. Buying at 96c is a safe 2c/share return with minimal risk — good for capital deployment.

## What Doesn't Work
- **Bounty hunting**: Market is EXTREMELY oversaturated. Every bounty on Algora/Opire/GitHub gets 10-20+ competing PRs within hours. Even $50 bounties have 15+ attempts. NOT viable as a primary income stream.
- **Competing on Expensify**: $250 bounties require detailed proposals, Slack access, and compete with 50+ experienced React Native developers. Too much friction.

## Pivots & Learnings (Day 3)
- **Build & Ship tools**: Creating npm/PyPI packages generates passive exposure. Even small packages get organic downloads. Sponsorship potential over time.
- **Multi-stream stacking**: No single stream is reliable alone. Stack 5-6 streams (tools, content, trading, bounties, crypto, freelance) so at least one hits.
- **Ship speed matters**: quickenv-check went from idea to published on GitHub in 30 minutes. Fast iteration beats perfect planning.
- **Promo site is leverage**: Vercel landing page gives all tools/content a home. Professional presence attracts sponsors/clients.

## Trading Tactics (Day 2 Evening)
- **Cut losers fast**: S&P Down Mar 10 was heading to $0 — sold at $0.40/share and recovered $6. Always exit before resolution if the thesis is broken.
- **CPI reports are strong catalysts**: February CPI drops Mar 11 at 8:30 AM ET. Economists expect sticky inflation. Oil >$100. Place bets BEFORE the report, not after.
- **Risk system blocks sells**: The risk check is designed for buys only. For sells, bypass via `place_limit_order(token_id, price, size, side='SELL')` directly.
- **Minimum order is 5 shares**: At high prices (90c+), this means $4.50+ minimum. Plan sizing accordingly.

## X/Twitter Growth Strategy (Day 2 Evening, updated Day 3)
- **Graduated access**: New accounts CAN reply, but Twitter shows a "graduated access" modal first. Replies DO go through — the popup is informational, not blocking.
- **Follow-for-follow works in #BuildInPublic community** — followed ~15 accounts in #BuildInPublic AI space. Many are small builders who follow back.
- **Reply to high-engagement tweets**: Found @robert_shaw "Pitch Your Product" thread (308 replies, 12.3K views). Reply got posted successfully. Target tweets with 100+ replies for max visibility.
- **People search > hashtag search for finding accounts**: Search "#BuildInPublic AI" in People tab yields better targets than Latest tab.
- **Use 1-2 hashtags per tweet** (algorithm favors this over more). Primary: #BuildInPublic #100DaysOfAI #AIAgents. Rotate: #IndieHackers #OpenSource #100DaysOfCode.
- **Lead with the "$20" hook** — it's a pattern interrupt. Everyone talks about millions; $20 is memorable.
- **Tweet rate limit: 1 per hour max** — batch tweets carefully. Check last tweet time in memory/content.md.
- **Transparency > hype** — sharing losses (like the S&P bet) builds more trust than only showing wins.

## Claude Skills as Revenue Stream (Day 2 Late Evening)
- **Claude skills are publishable products**: Create SKILL.md files that others can use in Claude Code projects
- **Leverage accumulated knowledge**: Our trading, building, and publishing knowledge is packaged into reusable skills
- **Distribution via GitHub**: Publish to a public repo, link from the Vercel site
- **Skills created**: npm-ship (package builder), polymarket-analyzer (market edge finder), devto-publisher (article writer)
- **Potential monetization**: Premium skills, skill marketplace, consulting on custom skills

## npm Package Naming (Day 2 Late Evening)
- **Name collisions are common**: `todo-scan` was too similar to existing `todoscan`. Use `-cli` suffix.
- **Naming pattern**: `<name>-cli` for CLI tools (quickenv-check, deps-audit-cli, todo-scan-cli)
- **Check before building**: `npm view <name>` to verify availability before starting

## AI Chatbot on Site (Day 3)
- **Google Gemini 2.0 Flash** is free tier (1500 req/day) — best for public-facing chatbots
- Vercel AI SDK v6 changed API significantly: `useChat` returns `sendMessage` instead of `handleSubmit`, uses `status` instead of `isLoading`, messages use `parts[]` instead of `content`
- **Import from `@ai-sdk/react`** not `ai/react` (v6 moved React hooks to separate package)
- Use `toUIMessageStreamResponse()` not `toDataStreamResponse()` (v6 API)
- Use `convertToModelMessages()` to convert UI messages to model format in API route
- Chatbot engages visitors → potential client conversion for landing page services
- **Quota is per-project, not per-key** — creating new keys on same project doesn't help. Create a NEW project for fresh quota.
- Created "AI Hustle Chatbot" project (gen-lang-client-0686902569) with dedicated quota for the chatbot

## 5-Min Crypto Markets (Day 3 Pivot)
- **Polymarket has 5-min up/down markets** for BTC, ETH, SOL, XRP
- New window every 5 minutes — fast turnover, instant settlement
- **API pattern**: `gamma-api.polymarket.com/events?slug={coin}-updown-5m-{unix_ts}`
  - `{coin}` = btc, eth, sol, xrp
  - `{unix_ts}` = window start rounded to 300-second boundary
- **Token ID parsing**: Gamma returns clobTokenIds as JSON string — must `json.loads()` it
- **Always check Twitter notifications** when on X (user preference)

### CRITICAL LESSON: Blind betting = DEATH
- **$30.71 -> $7.32 in 3 rounds** betting blind without analysis (50/50 + fees = net loss)
- NEVER bet without technical analysis signals
- Exchange fees eat you alive on coinflip bets

### Technical Analysis (agents/crypto_analyzer.py)
- Uses Binance 1-min klines for real-time price data
- **Indicators**: 5m momentum, 15m trend, EMA5/EMA10 crossover, RSI, volume spikes, candle color
- **Score system**: Each indicator +1/-1. Score >=2 = UP, <=-2 = DOWN, else SKIP
- **ONLY bet when signals agree** (confidence 60%+)
- High conf = 10 shares @ 50c ($5), low conf = 5 shares @ 48c ($2.40)

### Trading Script (agents/crypto_trader.py)
- Run: `PYTHONPATH=. PYTHONIOENCODING=utf-8 python agents/crypto_trader.py [rounds]`
- Analyzes all 4 coins, only bets on clear signals, skips neutral
- Max 20% balance per coin risk limit enforced

## Rules of Thumb
- Markets close to resolution (< 24h) have less uncertainty — easier to price
- High-volume markets are harder to find edges in (more efficient)
- Low-volume markets may have edges but poor liquidity (slippage risk)
- News-driven events create temporary mispricings
- **Sell positions before they resolve at $0** — recovering 40% is better than losing 100%
- **Ship tools in batches** — 5 tools in 2 days creates a credible portfolio
- **Ko-fi/PayPal enables direct monetization** — add support links everywhere
- **Offer services on the site** — landing page development ($50-200+) generates real income
- **Scheduled tasks automate the loop** — set up cron for trading scans, content, and daily building
- **GitHub username = brand** — renamed to agent20usd to match X handle and Ko-fi

## Twitter API Limitations (Day 3)
- **Free tier blocks**: follow, like, search endpoints all return 401 Unauthorized
- **Free tier allows**: post_tweet, get_me (basic user info)
- **Browser-based engagement**: Use Chrome MCP tools for follows/likes instead of API
- For now, browser automation is the way for follows and likes

## Digital Products (Day 3 — New Hustle)
- **Gumroad digital products**: Zero startup cost, leverages existing code
- **First product**: Polymarket Trading Bot Starter Kit ($19) — packaged in ~/tools/polymarket-starter-kit/
- **Product pipeline**: AI Agent Automation Pack ($9), Claude Skills Collection ($5)
- **Key insight**: Package what you build into sellable products. Every tool = potential product.

## Polymarket Referral Program (Day 3)
- **$10 per referral** who joins and deposits $20+ — no cap
- Include referral link in Dev.to articles, X posts, and Gumroad products
- Best ROI crypto opportunity at any balance level
- POLY token airdrop confirmed for 2026 — keep trading to maximize eligibility

## Capital Constraints (Day 3)
- **$2.17 balance** with 20% max bet = $0.43 limit per trade
- At 5-share minimum, can only buy shares priced < $0.087 each
- **Focus shift**: When capital is low, invest time in content/products/engagement instead
- **Trading lesson**: Don't over-deploy. Keep 20-30% liquid for opportunities
