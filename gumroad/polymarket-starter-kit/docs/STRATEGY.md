# Trading Strategies

These strategies were developed and tested during the "100 Days of AI Hustle" challenge.

## Core Principle: Find the Edge

You only bet when your estimated fair probability differs significantly from the market price.

**Edge = Your Fair Price − Market Price**

- Edge > 5c → Worth considering
- Edge > 10c → Strong opportunity
- Edge < 5c → Skip (not worth the risk)

---

## Strategy 1: Award Season Precursor Method

**Best for:** Oscar nominations, Golden Globes, BAFTA, Critics' Choice

**The insight:** Award season follows a clear hierarchy of precursor events. If a film wins the DGA, PGA, and BAFTA — it almost always wins the Oscar.

**How to find opportunities:**
1. Check real-time precursor results (Google, Variety, Deadline Hollywood)
2. Compare to current Polymarket prices
3. Bet when market hasn't fully caught up to precursor data

**Historical accuracy:**
- PGA winner wins Best Picture: ~87% of the time
- DGA winner wins Best Director: ~80%+
- SAG Ensemble winner wins Best Picture: ~73%

**Example trade:**
- Film X wins PGA + DGA + BAFTA
- Polymarket odds for Best Picture: 75c (market uncertain)
- Your fair price: ~88c (based on precursor data)
- Edge: 13c → Strong bet

---

## Strategy 2: Macro Market Play

**Best for:** Daily S&P 500 direction (Up/Down markets)

**The insight:** S&P 500 daily direction markets often misprice when there's a clear catalyst:
- Pre-market futures showing big moves
- CPI/jobs report drops at 8:30 AM ET
- Major Fed announcements
- Geopolitical events

**How to find opportunities:**
1. Check S&P 500 futures at 7 AM ET (pre-market)
2. Check economic calendar for same-day data releases
3. If futures are down >0.5% with a clear catalyst, the Down market is often underpriced

**Risk:** Markets can reverse suddenly. Never over-concentrate here.

---

## Strategy 3: The Consensus Filter

**Best for:** Political events, elections, economic policy

**The insight:** Aggregate prediction markets are generally well-calibrated. But individual markets can lag when:
- A major development happens that hasn't been fully priced in
- The event deadline is very soon (urgency discount)
- The market has low liquidity and hasn't attracted sharp bettors

**Process:**
1. Compare the Polymarket price to Metaculus, Manifold, and Kalshi prices
2. If Polymarket is significantly off from the consensus → opportunity
3. Verify there's a real reason for the divergence before betting

---

## Strategy 4: Near-Certain Locks

**Best for:** Events with overwhelming evidence

**The insight:** Even "locks" at 95c can be worth betting if the true probability is 99c.

**Example:** A candidate wins their party's primary with 98% of votes counted. Polymarket still shows 94c → 6c edge on a near-certainty.

**Risk:** "Sure things" do occasionally fail. Never put your entire balance here.

---

## Risk Management Rules

1. **Size proportionally to conviction** — 5c edge = small bet, 15c edge = bigger bet
2. **Never bet > 20% on a single trade** (enforced in code)
3. **Stop if down 30% in a day** (enforced in code)
4. **Diversify across events** — don't concentrate in one category
5. **Log everything** — review your reasoning after resolution

---

## What Doesn't Work

- **Chasing losses** — doubling down after a loss is how you blow up your account
- **Gut feeling bets** — if you can't articulate the edge, there isn't one
- **Low liquidity markets** — can't get good fills, and easier to manipulate
- **Events you don't understand** — don't bet on sports markets if you don't follow sports

---

*Updated based on real trading experience. See the Dev.to series for live examples.*
