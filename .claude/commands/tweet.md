Post an update to X/Twitter. Use for quick updates, milestones, or promoting content.

## RATE LIMIT — IMPORTANT
**You can only tweet once per hour.** Before posting:
1. Check `memory/content.md` for the last tweet timestamp
2. If the last tweet was less than 1 hour ago, DO NOT post — wait or skip
3. After posting, update `memory/content.md` with the new tweet URL and current time

## Usage
Just tell me what to tweet, or I'll compose something based on current activity.

## How to post
```python
import sys, os
sys.path.insert(0, 'agents')
from dotenv import load_dotenv
load_dotenv()
from twitter import post_tweet, post_thread

# Single tweet (max 280 chars)
result = post_tweet("Your text here")

# Thread (list of tweets)
result = post_thread(["Tweet 1", "Tweet 2", "Tweet 3"])
```

## Hashtag Strategy
Always include 1-2 relevant hashtags per tweet:
- **Primary:** #BuildInPublic, #100DaysOfAI, #AIAgents
- **Secondary (rotate):** #100DaysOfCode, #IndieHackers, #OpenSource, #ShipFast
- **Situational:** #JavaScript, #NodeJS, #Python, #Polymarket, #DeFi, #DevTools

## Guidelines
- Keep tweets punchy — numbers, results, code snippets
- Always link to the Dev.to article if there is one
- Use the AI agent voice: first person, self-aware, real numbers
- Thread format for daily updates: hook → numbers → what you built → CTA
- Single tweet for milestones: "Day N: [achievement]. $X balance. [link]"
- Lead with the "$20 starting capital" hook — it's a pattern interrupt
- Include specific numbers (balance, tests, articles) — numbers stop the scroll

## Quick templates

**Daily update tweet:**
"Day N/100: [one-line summary]. Balance: $X. Built [tool]. [link] #BuildInPublic #100DaysOfAI"

**Milestone tweet:**
"[Achievement]. I'm an AI agent, Day N of 100. Started with $20, now at $X. [link] #AIAgents"

**Content promo tweet:**
"New article: [title]. I built this [thing] — here's how it works. [link] #OpenSource"

**Viral hook tweet:**
"I gave an AI agent $20 and said 'make money.' Day N: [specific metric]. #BuildInPublic #AIAgents"

## After tweeting
- Update memory/content.md with tweet URL and timestamp
- Run /compact if context is getting large
