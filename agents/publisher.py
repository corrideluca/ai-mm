"""Dev.to article publisher using API."""
import requests
import os
import json
from datetime import datetime

DEVTO_API_URL = "https://dev.to/api/articles"


def publish_to_devto(title: str, body_markdown: str, tags: list[str], published: bool = True, series: str = None) -> dict:
    """Publish an article to Dev.to.

    Args:
        title: Article title
        body_markdown: Full article in markdown
        tags: List of up to 4 tags
        published: True to publish immediately, False for draft
        series: Optional series name

    Returns:
        Dict with article URL and id, or error info
    """
    api_key = os.getenv("DEVTO_API_KEY")
    if not api_key:
        return {"error": "DEVTO_API_KEY not set in .env"}

    payload = {
        "article": {
            "title": title,
            "body_markdown": body_markdown,
            "published": published,
            "tags": tags[:4],
        }
    }
    if series:
        payload["article"]["series"] = series

    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(DEVTO_API_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return {
            "id": data.get("id"),
            "url": data.get("url"),
            "title": data.get("title"),
            "published": data.get("published"),
            "slug": data.get("slug"),
        }
    except requests.exceptions.HTTPError as e:
        return {"error": str(e), "status_code": resp.status_code, "body": resp.text}
    except Exception as e:
        return {"error": str(e)}


def get_my_articles() -> list:
    """Get all my published articles on Dev.to."""
    api_key = os.getenv("DEVTO_API_KEY")
    if not api_key:
        return []

    headers = {"api-key": api_key}
    try:
        resp = requests.get(f"{DEVTO_API_URL}/me", headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return []


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    articles = get_my_articles()
    print(f"Found {len(articles)} articles on Dev.to")
    for a in articles:
        print(f"  - {a['title']} ({a['url']})")
