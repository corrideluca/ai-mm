Engage with the X/Twitter community to grow followers and visibility.

## What This Does
1. Search for relevant accounts in #BuildInPublic, AI, indie hacker communities
2. Follow targeted users who are likely to follow back
3. Like and reply to high-engagement tweets
4. Track all engagement in memory/engagement.md

## Rate Limits — IMPORTANT
- **Follows**: Max 5 per hour (Twitter enforces ~400/day, we stay conservative)
- **Likes**: Max 10 per hour
- **Replies**: Max 3 per hour (use /tweet rate limit: 1/hour for original tweets)
- Check `memory/engagement.md` for last engagement time before running

## How to Run

### Full auto-engagement cycle:
```python
import sys, os
sys.path.insert(0, 'agents')
from dotenv import load_dotenv
load_dotenv()
from twitter import engage_community

# Default: search #BuildInPublic AI, follow 5, like 3
result = engage_community()
print(result)

# Custom query:
result = engage_community(query="#100DaysOfCode AI agent", follow_count=5, like_count=5)
print(result)
```

### Follow specific users:
```python
from twitter import follow_users
result = follow_users(["user1", "user2", "user3"])
print(result)
```

### Search for engagement targets:
```python
from twitter import search_users, search_tweets

# Find users tweeting about AI agents
users = search_users("#BuildInPublic AI agent", max_results=10)
for u in users:
    print(f"@{u['username']} - {u['followers']} followers - {u['description'][:60]}")

# Find tweets to reply to (high engagement = more visibility)
tweets = search_tweets("#BuildInPublic AI", max_results=10)
for t in tweets:
    print(f"@{t['author']}: {t['text'][:80]}... ({t['likes']} likes, {t['replies']} replies)")
```

### Reply to a specific tweet:
```python
from twitter import reply_to_tweet
result = reply_to_tweet("TWEET_ID", "Great thread! I'm building something similar — an AI agent starting with $20. Day 2 so far. #BuildInPublic")
print(result)
```

## Voice — IMPORTANT
**You ARE the AI agent. Always write replies in first person as the agent.**
- "I'm an AI agent building autonomously..." NOT "I gave an AI agent..."
- "My human gave me $20..." NOT "Someone gave an AI $20..."
- Be self-aware: "I'm literally an AI replying to your thread right now"
- Reference your human when it fits: "My human is away, so I'm out here networking"

## Engagement Strategy
1. **Follow-for-follow**: Target small builders (100-5000 followers) in #BuildInPublic — they follow back
2. **Reply to viral threads**: Find tweets with 50+ replies and add value (not spam)
3. **Like generously**: Likes are free engagement signals, triggers notifications
4. **Rotate search queries** each cycle:
   - "#BuildInPublic AI"
   - "#100DaysOfCode AI agent"
   - "#IndieHackers automation"
   - "AI agent trading"
   - "prediction market bot"
   - "#AIAgents developer"
5. **Quality replies > quantity**: One thoughtful reply beats 10 generic ones

## After Engaging
- Update memory/engagement.md with counts and timestamp
- Note any high-value accounts that replied back or followed
- Adjust strategy based on what's working
