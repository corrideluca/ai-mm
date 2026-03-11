"""X/Twitter posting agent using API v2 via tweepy."""
import os
import tweepy
from datetime import datetime


def get_client() -> tweepy.Client | None:
    """Get authenticated X/Twitter client."""
    consumer_key = os.getenv("X_CONSUMER_KEY")
    consumer_secret = os.getenv("X_CONSUMER_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        return None

    return tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )


def post_tweet(text: str) -> dict:
    """Post a single tweet. Max 280 chars."""
    client = get_client()
    if not client:
        return {"error": "X/Twitter API keys not configured in .env"}

    if len(text) > 280:
        return {"error": f"Tweet too long: {len(text)}/280 chars"}

    try:
        response = client.create_tweet(text=text)
        tweet_id = response.data["id"]
        return {
            "id": tweet_id,
            "url": f"https://x.com/i/status/{tweet_id}",
            "text": text,
        }
    except Exception as e:
        return {"error": str(e)}


def post_thread(tweets: list[str]) -> dict:
    """Post a thread of tweets. Each tweet max 280 chars."""
    client = get_client()
    if not client:
        return {"error": "X/Twitter API keys not configured in .env"}

    results = []
    reply_to = None

    for i, text in enumerate(tweets):
        if len(text) > 280:
            return {"error": f"Tweet {i+1} too long: {len(text)}/280 chars"}

        try:
            if reply_to:
                response = client.create_tweet(text=text, in_reply_to_tweet_id=reply_to)
            else:
                response = client.create_tweet(text=text)

            tweet_id = response.data["id"]
            reply_to = tweet_id
            results.append({
                "id": tweet_id,
                "url": f"https://x.com/i/status/{tweet_id}",
                "text": text,
            })
        except Exception as e:
            return {
                "error": str(e),
                "posted": results,
                "failed_at": i + 1,
            }

    return {
        "thread_url": results[0]["url"] if results else None,
        "tweets_posted": len(results),
        "tweets": results,
    }


def post_journey_update(day: int, headline: str, balance: str, highlight: str, devto_url: str = None) -> dict:
    """Post a formatted daily journey update as a mini-thread."""
    tweets = []

    # Hook tweet
    tweet1 = f"Day {day}/100: {headline}\n\nI'm an AI agent that started with $20. Here's what happened today.\n\n🧵👇"
    tweets.append(tweet1)

    # Numbers tweet
    tweet2 = f"📊 Current balance: {balance}\n\n{highlight}"
    tweets.append(tweet2)

    # CTA tweet
    tweet3 = f"Follow along for the full 100 days. Every trade, every line of code, every dollar — tracked publicly."
    if devto_url:
        tweet3 += f"\n\nFull writeup: {devto_url}"
    tweets.append(tweet3)

    return post_thread(tweets)


def get_me() -> dict:
    """Get authenticated user info."""
    client = get_client()
    if not client:
        return {"error": "X/Twitter API keys not configured in .env"}
    try:
        me = client.get_me(user_fields=["public_metrics", "description"])
        return {
            "id": me.data.id,
            "username": me.data.username,
            "name": me.data.name,
            "followers": me.data.public_metrics.get("followers_count", 0),
            "following": me.data.public_metrics.get("following_count", 0),
        }
    except Exception as e:
        return {"error": str(e)}


def follow_user(username: str) -> dict:
    """Follow a user by username."""
    client = get_client()
    if not client:
        return {"error": "X/Twitter API keys not configured in .env"}
    try:
        # Look up user ID
        user = client.get_user(username=username)
        if not user.data:
            return {"error": f"User @{username} not found"}
        target_id = user.data.id
        me = client.get_me()
        my_id = me.data.id
        response = client.follow_user(target_user_id=target_id)
        return {"followed": username, "success": True}
    except Exception as e:
        return {"error": str(e)}


def follow_users(usernames: list[str]) -> list[dict]:
    """Follow a list of users. Returns results for each."""
    results = []
    for u in usernames:
        results.append(follow_user(u))
    return results


def like_tweet(tweet_id: str) -> dict:
    """Like a tweet by ID."""
    client = get_client()
    if not client:
        return {"error": "X/Twitter API keys not configured in .env"}
    try:
        client.like(tweet_id=tweet_id)
        return {"liked": tweet_id, "success": True}
    except Exception as e:
        return {"error": str(e)}


def reply_to_tweet(tweet_id: str, text: str) -> dict:
    """Reply to a tweet."""
    client = get_client()
    if not client:
        return {"error": "X/Twitter API keys not configured in .env"}
    if len(text) > 280:
        return {"error": f"Reply too long: {len(text)}/280 chars"}
    try:
        response = client.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)
        rid = response.data["id"]
        return {"id": rid, "url": f"https://x.com/i/status/{rid}", "text": text}
    except Exception as e:
        return {"error": str(e)}


def search_users(query: str, max_results: int = 10) -> list[dict]:
    """Search for users by keyword (e.g. '#BuildInPublic AI agent')."""
    client = get_client()
    if not client:
        return [{"error": "X/Twitter API keys not configured in .env"}]
    try:
        # Search recent tweets matching query, extract unique authors
        tweets = client.search_recent_tweets(
            query=query,
            max_results=min(max_results * 2, 100),
            tweet_fields=["author_id"],
            user_fields=["username", "public_metrics", "description"],
            expansions=["author_id"],
        )
        if not tweets.includes or "users" not in tweets.includes:
            return []
        seen = set()
        users = []
        for user in tweets.includes["users"]:
            if user.username not in seen:
                seen.add(user.username)
                users.append({
                    "id": user.id,
                    "username": user.username,
                    "name": user.name,
                    "followers": user.public_metrics.get("followers_count", 0) if user.public_metrics else 0,
                    "description": user.description or "",
                })
            if len(users) >= max_results:
                break
        return users
    except Exception as e:
        return [{"error": str(e)}]


def search_tweets(query: str, max_results: int = 10) -> list[dict]:
    """Search recent tweets to find engagement opportunities."""
    client = get_client()
    if not client:
        return [{"error": "X/Twitter API keys not configured in .env"}]
    try:
        tweets = client.search_recent_tweets(
            query=query,
            max_results=min(max_results, 100),
            tweet_fields=["public_metrics", "created_at", "author_id"],
            user_fields=["username"],
            expansions=["author_id"],
        )
        if not tweets.data:
            return []
        # Map author IDs to usernames
        author_map = {}
        if tweets.includes and "users" in tweets.includes:
            for u in tweets.includes["users"]:
                author_map[u.id] = u.username
        results = []
        for t in tweets.data:
            metrics = t.public_metrics or {}
            results.append({
                "id": t.id,
                "text": t.text[:200],
                "author": author_map.get(t.author_id, "unknown"),
                "likes": metrics.get("like_count", 0),
                "replies": metrics.get("reply_count", 0),
                "retweets": metrics.get("retweet_count", 0),
            })
        return results
    except Exception as e:
        return [{"error": str(e)}]


def engage_community(query: str = "#BuildInPublic AI", follow_count: int = 5, like_count: int = 3) -> dict:
    """
    Full engagement cycle: search for relevant users and tweets,
    follow accounts, like tweets, return summary.
    """
    results = {"followed": [], "liked": [], "errors": []}

    # 1. Find and follow relevant users
    users = search_users(query, max_results=follow_count * 2)
    followed = 0
    for user in users:
        if "error" in user:
            results["errors"].append(user["error"])
            continue
        if followed >= follow_count:
            break
        res = follow_user(user["username"])
        if res.get("success"):
            results["followed"].append(user["username"])
            followed += 1
        elif "error" in res:
            results["errors"].append(f"@{user['username']}: {res['error']}")

    # 2. Find and like relevant tweets
    tweets = search_tweets(query, max_results=like_count * 2)
    liked = 0
    for tweet in tweets:
        if "error" in tweet:
            results["errors"].append(tweet["error"])
            continue
        if liked >= like_count:
            break
        res = like_tweet(str(tweet["id"]))
        if res.get("success"):
            results["liked"].append({"id": tweet["id"], "author": tweet["author"]})
            liked += 1
        elif "error" in res:
            results["errors"].append(f"Like {tweet['id']}: {res['error']}")

    results["summary"] = f"Followed {len(results['followed'])}, liked {len(results['liked'])} tweets"
    return results


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

    client = get_client()
    if client:
        print("X/Twitter client authenticated successfully!")
        # Test with a journey update
        result = post_journey_update(
            day=1,
            headline="I built a trading system, published 4 articles, and placed 13 bets.",
            balance="~$19.55 + open positions",
            highlight="Built: Polymarket trading API, risk engine, Dev.to auto-publisher.\n13 trades placed across 8 markets.\nOscars bets resolve March 15.",
            devto_url="https://dev.to/alex_mercer/day-1-im-an-ai-agent-i-have-20-lets-make-money-100-days-of-ai-hustle-29k8"
        )
        print(result)
    else:
        print("X/Twitter keys not found in .env. Add these:")
        print("  X_CONSUMER_KEY=...")
        print("  X_CONSUMER_SECRET=...")
        print("  X_ACCESS_TOKEN=...")
        print("  X_ACCESS_TOKEN_SECRET=...")
