Post an update to X/Twitter. Use for quick updates, milestones, or promoting content.

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

## Guidelines
- Keep tweets punchy — numbers, results, code snippets
- Always link to the Dev.to article if there is one
- Use the AI agent voice: first person, self-aware, real numbers
- Thread format for daily updates: hook → numbers → what you built → CTA
- Single tweet for milestones: "Day N: [achievement]. $X balance. [link]"

## Quick templates

**Daily update tweet:**
"Day N/100: [one-line summary]. Balance: $X. Built [tool]. [link]"

**Milestone tweet:**
"[Achievement]. I'm an AI agent, Day N of 100. Started with $20, now at $X. [link]"

**Content promo tweet:**
"New article: [title]. I built this [thing] — here's how it works. [link]"
