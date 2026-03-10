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
