"""News agent — searches the web for relevant news before placing bets."""

from core import cache


def research_topic(query: str, max_results: int = 5) -> dict:
    """
    Placeholder that returns a search query for Claude to execute via WebSearch.

    Claude Code has WebSearch built in — this agent just structures
    the request and caches results so we don't re-search the same topic.
    """
    cache_key = f"news_{query[:50]}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    # Return the query for Claude to run via its WebSearch tool
    return {
        "query": query,
        "max_results": max_results,
        "cached": False,
        "instructions": (
            "Use WebSearch to find recent news about this topic. "
            "Summarize key facts that could affect the market outcome."
        ),
    }


def cache_research(query: str, summary: str) -> None:
    """Cache research results so we don't re-search the same topic."""
    cache_key = f"news_{query[:50]}"
    cache.set(cache_key, {"query": query, "summary": summary, "cached": True})
