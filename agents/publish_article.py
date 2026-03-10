"""Publish an article to Dev.to from a markdown file."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from publisher import publish_to_devto
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def publish_from_file(filepath, title, tags, series=None):
    with open(filepath) as f:
        body = f.read()
    return publish_to_devto(title=title, body_markdown=body, tags=tags, series=series)

if __name__ == "__main__":
    # Usage: python publish_article.py <filepath> <title> <tag1,tag2,...> [series]
    if len(sys.argv) < 4:
        print("Usage: python publish_article.py <filepath> <title> <tag1,tag2,...> [series]")
        sys.exit(1)
    filepath = sys.argv[1]
    title = sys.argv[2]
    tags = sys.argv[3].split(",")
    series = sys.argv[4] if len(sys.argv) > 4 else None
    result = publish_from_file(filepath, title, tags, series)
    print(result)
