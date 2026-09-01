"""Find a reputable seller on the public web when catalog stores miss.

If no live search API key is configured, returns an honest non-live hint
instead of fabricated product prices.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

import requests

logger = logging.getLogger(__name__)


class WebSourceService:
    def search(
        self,
        query: str,
        country: Optional[str] = None,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        api_key = os.getenv("TAVILY_API_KEY", "").strip()
        if api_key:
            live = self._tavily_search(query, country, api_key, limit)
            if live:
                return live

        ddg = self._duckduckgo(query, country, limit)
        if ddg:
            return ddg

        locale = country or "worldwide"
        q = quote_plus(f"{query} buy official store {locale}")
        return [
            {
                "title": f"منبع اینترنتی برای «{query}» (جستجوی زنده پیکربندی نشده)",
                "price": None,
                "url": f"https://duckduckgo.com/?q={q}",
                "store": "web_fallback",
                "availability": None,
                "score": None,
                "specs": {
                    "source_type": "suggested_search",
                    "note": "برای نتایج زنده TAVILY_API_KEY را در محیط قرار دهید.",
                    "country": locale,
                },
                "is_live": False,
            }
        ]

    def _tavily_search(
        self, query: str, country: Optional[str], api_key: str, limit: int
    ) -> List[Dict[str, Any]]:
        try:
            resp = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": api_key,
                    "query": f"{query} official retailer {country or ''}".strip(),
                    "max_results": limit,
                    "include_answer": False,
                },
                timeout=12,
            )
            if resp.status_code != 200:
                logger.warning("Tavily error %s: %s", resp.status_code, resp.text[:200])
                return []
            payload = resp.json()
            items = []
            for row in payload.get("results") or []:
                items.append(
                    {
                        "title": row.get("title") or query,
                        "price": None,
                        "url": row.get("url"),
                        "store": "web_search",
                        "availability": None,
                        "score": row.get("score"),
                        "specs": {
                            "snippet": (row.get("content") or "")[:280],
                            "source_type": "live_web",
                        },
                        "is_live": True,
                    }
                )
            return items[:limit]
        except Exception as exc:
            logger.warning("Tavily search failed: %s", exc)
            return []

    def _duckduckgo(
        self, query: str, country: Optional[str], limit: int
    ) -> List[Dict[str, Any]]:
        q = f"{query} buy {country or ''}".strip()
        try:
            resp = requests.get(
                "https://api.duckduckgo.com/",
                params={"q": q, "format": "json", "no_html": 1, "skip_disambig": 1},
                timeout=10,
            )
            if resp.status_code != 200:
                return []
            data = resp.json()
            items: List[Dict[str, Any]] = []
            if data.get("AbstractURL"):
                items.append(
                    {
                        "title": data.get("Heading") or query,
                        "price": None,
                        "url": data.get("AbstractURL"),
                        "store": "web_search",
                        "availability": None,
                        "score": None,
                        "specs": {
                            "snippet": (data.get("AbstractText") or "")[:280],
                            "source_type": "live_web",
                        },
                        "is_live": True,
                    }
                )
            for topic in data.get("RelatedTopics") or []:
                if not isinstance(topic, dict):
                    continue
                url = topic.get("FirstURL")
                text = topic.get("Text")
                if url and text:
                    items.append(
                        {
                            "title": text[:120],
                            "price": None,
                            "url": url,
                            "store": "web_search",
                            "availability": None,
                            "score": None,
                            "specs": {"source_type": "live_web"},
                            "is_live": True,
                        }
                    )
                if len(items) >= limit:
                    break
            return items[:limit]
        except Exception as exc:
            logger.warning("DuckDuckGo lookup failed: %s", exc)
            return []
