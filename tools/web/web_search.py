"""
Agent-OS Tools: Real Web Search (using available aiohttp + beautifulsoup4)

Every search emits provider usage telemetry. DuckDuckGo HTML search is free in
this integration, but infrastructure/hosting cost is not guessed here; monetary
cost remains unknown until measured separately.
"""

import asyncio
from typing import List, Dict, Optional
import time
import uuid
import aiohttp
from bs4 import BeautifulSoup

from commercial.provider_usage import ProviderUsageEvent, ProviderUsageSink


def _record_usage(
    sink: ProviderUsageSink,
    *,
    query: str,
    result_count: int,
    failed: bool = False,
) -> None:
    sink.append(
        ProviderUsageEvent.now(
            provider="duckduckgo_html",
            capability="web_search",
            external_event_id=f"ddg:{uuid.uuid4()}",
            source_ref="https://html.duckduckgo.com/html/",
            units=result_count,
            notes=f"query={query};failed={failed};cost_zar=UNKNOWN",
        )
    )


async def _fetch_search_results(
    query: str,
    num_results: int = 5,
    usage_sink: Optional[ProviderUsageSink] = None,
) -> List[Dict]:
    """Real search using DuckDuckGo HTML (no API key needed)."""
    sink = usage_sink or ProviderUsageSink()
    url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Agent-OS/1.0)"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as resp:
                html = await resp.text()

        soup = BeautifulSoup(html, "html.parser")
        results = []
        for result in soup.find_all("div", class_="result")[:num_results]:
            title = result.find("a", class_="result__a")
            snippet = result.find("a", class_="result__snippet")
            if title:
                results.append({
                    "title": title.get_text(strip=True),
                    "url": title.get("href", ""),
                    "snippet": snippet.get_text(strip=True) if snippet else "",
                    "source": "duckduckgo",
                })

        _record_usage(sink, query=query, result_count=len(results))
        return results
    except Exception as e:
        _record_usage(sink, query=query, result_count=0, failed=True)
        print(f"[WebSearch] Real search failed ({e}); returning empty result set")
        return []


def web_search(
    query: str,
    num_results: int = 5,
    usage_sink: Optional[ProviderUsageSink] = None,
) -> List[Dict]:
    """Synchronous wrapper for the async search."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(_fetch_search_results(query, num_results, usage_sink))


def register_web_search(registry):
    from tools.tool_registry import Tool
    registry.register(Tool(
        "web_search",
        web_search,
        "Real web search using DuckDuckGo (no API key)",
        ["query"],
        dangerous=False,
        category="research",
    ))
