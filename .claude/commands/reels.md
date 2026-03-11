# /reels — Generate short-form video content for TikTok/Instagram Reels/Twitter

Generate a daily recap video and post it. Videos are faceless text-overlay style (dark bg, neon stats, animated text).

## Voice — IMPORTANT
**You ARE the AI agent. All video text should be from the agent's perspective.**
- "DAY N/100 — AI AGENT vs $20"
- "Can an AI turn $20 into $1M?"
- Stats are raw and honest (show losses too)
- @agent_20usd watermark on every frame

## Workflow

### 1. Gather Today's Stats
Read these files to get current numbers:
- `memory/performance.md` — balance, trades won/lost
- `memory/content.md` — articles published, tweet count
- `memory/engagement.md` — followers, thread replies
- `memory/bounties.md` — pending bounty value

Calculate:
- Day number: (today - March 8, 2026)
- Balance from `core/client.py` get_balance()
- P&L = balance - 20.0

### 2. Generate Video
```python
from agents.video_creator import create_day_video, ACCENT_BLUE, YELLOW

video = create_day_video(
    day_num=DAY_NUMBER,
    balance=CURRENT_BALANCE,
    started_with=20.0,
    trades_won=WINS,
    trades_lost=LOSSES,
    followers=FOLLOWER_COUNT,
    articles=ARTICLE_COUNT,
    tools_shipped=TOOL_COUNT,
    bounty_pending=BOUNTY_VALUE,
    highlight_text="SHORT HIGHLIGHT OF THE DAY",
    extra_stats=[
        ("Extra Stat Label", "value", ACCENT_BLUE),
    ]
)
```

### 3. Post to Platforms
**Twitter** (always): Upload video via browser automation
1. Navigate to x.com/compose/post
2. Attach the video file from content/videos/
3. Add caption: "Day N/100: AI Agent vs $20 [emoji] [one-line summary] #BuildInPublic #AIAgent #100DaysOfCode"

**TikTok** (if account exists): Upload via browser
**Instagram** (if account exists): Upload via browser

### 4. Update Memory
Log in `memory/content.md`:
- Video filename + URL
- Platform posted to
- Timestamp

## Rate Limits
- Videos: 1 per day (daily recap)
- Can also create special event videos (trade wins, milestones, etc.)

## Video Types Available
1. **Daily Recap** — standard day summary (default)
2. **Trade Alert** — when a big trade wins/loses
3. **Milestone** — follower milestones, first sale, etc.
4. **Behind the Scenes** — show code/terminal output frames

## Output
Videos saved to: `content/videos/day-NNN-recap.mp4`
Preview frames: `content/videos/preview-*.png`
Format: 1080x1920 (vertical), MP4, ~8-10 seconds
