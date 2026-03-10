Create money-making content autonomously. Write articles, social media threads, and SEO content.

## RATE LIMIT — IMPORTANT
**You can only publish ONE article every 6 hours.** Before publishing:
1. Check `memory/content.md` for the last article publish timestamp
2. If the last article was published less than 6 hours ago, DO NOT publish — wait or skip
3. After publishing, update `memory/content.md` with the new article URL and current time
4. Add a line: `**LAST ARTICLE TIME: [timestamp]**`

## Step 1: Find trending topics
Use WebSearch to research what's trending RIGHT NOW:
- Search: "trending topics today {current_date}"
- Search: "viral tech news this week"
- Search: "trending on hacker news today"
- Search: "most searched topics google trends today"

## Step 2: Pick the best topic
Choose a topic that is:
- Currently trending (timing matters)
- Something you have genuine knowledge about
- Has monetization potential (affiliate links, product recommendations)
- Not oversaturated (find a unique angle)

## Step 3: Create the content
Write ONE of these content types (pick the best fit):

### Option A: Long-form article (for Medium/blog)
- 1500-2500 words, well-structured with headers
- SEO-optimized title and meta description
- Include actionable insights, not just fluff
- Save to /Users/corri/content/articles/

### Option B: Twitter/X thread (for social engagement)
- 8-15 tweets, each standalone but building a narrative
- Hook in first tweet, value throughout, CTA at end
- Save to /Users/corri/content/threads/

### Option C: Technical tutorial
- Step-by-step guide solving a real problem
- Include code samples
- Save to /Users/corri/content/tutorials/

### Option D: Newsletter edition
- Curated digest of top stories + your analysis
- 5-7 stories with commentary
- Save to /Users/corri/content/newsletters/

## Step 4: Publish (if accounts are configured)
- Check if any publishing APIs/CLIs are configured
- If Medium token exists in .env, publish via API
- If Twitter/X credentials exist, post thread
- Otherwise, save content for manual publishing

## Step 5: Track content
Update memory/content.md with:
- What was created, topic, type
- Where it was published (or saved for publishing)
- Any engagement metrics if available

## Content strategy notes:
- AI/tech tutorials get the most engagement
- Listicles with practical tips perform well
- Controversial takes drive engagement but can backfire
- Always provide genuine value — no clickbait without substance
