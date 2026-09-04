from __future__ import annotations
import gzip
import json
import html
import re
import urllib.parse
import urllib.request
import zlib
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import List, Optional
@dataclass
class WebEvidence:
    title: str
    url: str
    source: str
    snippet: str
    content: str
    reliability_score: float = 0.0
    reliability_level: str = "unknown"
    verification_status: str = "unverified"


def _get_source_reliability(url: str) -> tuple[float, str]:
    """
    Estimate source reliability from the website domain.

    This is a source-quality signal only.
    It does NOT mean that every claim on a high-reliability
    domain is automatically true.
    """
    try:
        hostname = urllib.parse.urlparse(url or "").hostname or ""
        hostname = hostname.lower().strip(".")
    except Exception:
        hostname = ""

    if not hostname:
        return 0.0, "unknown"

    # Highly authoritative / primary sources
    high_domains = (
        "python.org",
        "wikipedia.org",
        "gov",
        "who.int",
        "un.org",
        "nasa.gov",
        "nih.gov",
        "cdc.gov",
        "fda.gov",
        "edu",
    )

    # Generally reliable secondary/reference sources
    medium_domains = (
        "w3schools.com",
        "geeksforgeeks.org",
        "britannica.com",
        "reuters.com",
        "apnews.com",
        "bbc.com",
        "bbc.co.uk",
        "accuweather.com",
        "meteoblue.com",
        "weather.com",
        "wmo.int",
        "weather.gov",
    )

    if hostname.endswith(".gov") or hostname.endswith(".edu"):
        return 0.95, "high"

    if any(
        hostname == domain or hostname.endswith("." + domain)
        for domain in high_domains
    ):
        return 0.90, "high"

    if any(
        hostname == domain or hostname.endswith("." + domain)
        for domain in medium_domains
    ):
        return 0.75, "medium"

    return 0.50, "unknown"



def _verify_evidence_agreement(
    evidence: List[WebEvidence],
) -> List[WebEvidence]:
    """
    Verify evidence conservatively using meaningful keyword overlap
    across independent domains.
    Source reliability and factual verification are separate:
    a highly reliable source is not automatically true.
    Verification requires independent corroboration.
    """
    if not evidence:
        return evidence
    stopwords = {
        "about", "after", "again", "also", "been", "being",
        "between", "could", "does", "from", "have", "into",
        "more", "most", "other", "over", "such", "than",
        "that", "their", "there", "these", "they", "this",
        "those", "through", "used", "using", "were", "which",
        "while", "with", "would", "your", "what", "when",
        "where", "whose", "very", "only", "can", "may",
        "might", "will", "its", "our", "their", "you",
        "how", "why", "does", "did", "not", "but", "for",
        "the", "and", "are", "was", "has", "had", "into",
    }
    def normalize_words(text: str) -> set[str]:
        text = (text or "").lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return {
            word
            for word in text.split()
            if len(word) >= 4 and word not in stopwords
        }
    def get_domain(url: str) -> str:
        try:
            hostname = urllib.parse.urlparse(url or "").hostname or ""
            hostname = hostname.lower().strip(".")
        except Exception:
            hostname = ""
        if hostname.startswith("www."):
            hostname = hostname[4:]
        return hostname
    normalized_data = []
    for item in evidence:
        text = item.content or item.snippet
        words = normalize_words(text)
        normalized_data.append(
            {
                "words": words,
                "domain": get_domain(item.url),
                "reliability_score": item.reliability_score,
            }
        )
    for index, item in enumerate(evidence):
        current = normalized_data[index]
        current_words = current["words"]
        current_domain = current["domain"]
        if len(current_words) < 3 or not current_domain:
            item.verification_status = "unverified"
            continue
        corroborating_domains = set()
        for other_index, other in enumerate(evidence):
            if index == other_index:
                continue
            other_data = normalized_data[other_index]
            other_domain = other_data["domain"]
            # Only independent domains can corroborate one another.
            if not other_domain or other_domain == current_domain:
                continue
            other_words = other_data["words"]
            if len(other_words) < 3:
                continue
            shared_words = current_words.intersection(other_words)
            if len(shared_words) < 2:
                continue
            smaller_size = min(
                len(current_words),
                len(other_words),
            )
            if smaller_size <= 0:
                continue
            overlap_ratio = len(shared_words) / smaller_size
            # A corroborating source should itself have at least
            # medium source reliability. Unknown sources alone should
            # not be enough to mark evidence as corroborated.
            other_reliability = other_data["reliability_score"]
            strong_keyword_match = (
                len(shared_words) >= 3
                and overlap_ratio >= 0.25
            )
            moderate_keyword_match = (
                len(shared_words) >= 2
                and overlap_ratio >= 0.40
            )
            reliable_corroboration = other_reliability >= 0.75
            if (
                reliable_corroboration
                and (
                    strong_keyword_match
                    or moderate_keyword_match
                )
            ):
                corroborating_domains.add(other_domain)
        if corroborating_domains:
            item.verification_status = "corroborated"
        else:
            item.verification_status = "unverified"
    return evidence
class _HTMLTextParser(HTMLParser):
    """
    HTML -> readable text extractor.
    Removes common navigation/advertisement/UI containers while
    preserving article/main content.
    """
    SKIP_TAGS = {
        "script",
        "style",
        "noscript",
        "svg",
        "template",
        "head",
        "nav",
        "footer",
        "form",
        "button",
        "dialog",
        "iframe",
        "canvas",
    }
    BLOCK_TAGS = {
        "article",
        "section",
        "main",
        "p",
        "div",
        "li",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "blockquote",
        "pre",
        "br",
        "tr",
        "td",
        "th",
    }
    NOISE_WORDS = {
        "advert",
        "advertisement",
        "ads",
        "ad-container",
        "ad-wrapper",
        "banner",
        "breadcrumb",
        "cookie",
        "cookies",
        "comment",
        "comments",
        "dialog",
        "drawer",
        "footer",
        "header",
        "login",
        "menu",
        "modal",
        "navigation",
        "navbar",
        "newsletter",
        "popup",
        "promo",
        "promotion",
        "related-posts",
        "search",
        "share",
        "sidebar",
        "social",
        "subscribe",
        "subscription",
        "toolbar",
        "top-nav",
        "user-menu",
    }


    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: List[str] = []
        self.skip_depth = 0
        self.block_depth = 0



    def _attribute_text(self, attrs) -> str:
        values = []
        for key, value in attrs:
            if key in {"id", "class", "role", "aria-label", "data-testid"}:
                if value:
                    values.append(str(value).lower())
        return " ".join(values)


    
    def _is_noise_container(self, attrs) -> bool:
        text = self._attribute_text(attrs)
        if not text:
            return False
        tokens = set(re.findall(r"[a-z0-9_-]+", text))
        if tokens.intersection(self.NOISE_WORDS):
            return True
        patterns = (
            r"\bside[-_ ]?bar\b",
            r"\bnav(?:igation)?[-_ ]?(?:bar|menu)?\b",
            r"\b(?:top|main)[-_ ]?menu\b",
            r"\b(?:ad|ads)[-_ ]?(?:slot|box|container|wrapper)?\b",
            r"\b(?:cookie|consent)[-_ ]?(?:banner|box|popup)?\b",
            r"\b(?:login|sign[-_ ]?in)[-_ ]?(?:box|panel|modal)?\b",
            r"\bshare[-_ ]?(?:buttons?|bar|tools?)\b",
        )
        return any(re.search(pattern, text) for pattern in patterns)


    
    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if self.skip_depth:
            self.skip_depth += 1
            return
        if tag in self.SKIP_TAGS or self._is_noise_container(attrs):
            self.skip_depth = 1
            return
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")
            self.block_depth += 1



    def handle_startendtag(self, tag, attrs):
        if not self.skip_depth and tag.lower() in self.BLOCK_TAGS:
            self.parts.append("\n")


    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.skip_depth:
            self.skip_depth -= 1
            return
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")
            if self.block_depth > 0:
                self.block_depth -= 1


    def handle_data(self, data):
        if self.skip_depth:
            return
        text = data.strip()
        if text:
            self.parts.append(text)


    def get_text(self) -> str:
        return "\n".join(self.parts)

    
class WebResearch:

    def _http_get(self, url: str, headers=None, timeout: int = 15) -> str:
        request_headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;"
                "q=0.9,image/avif,image/webp,*/*;q=0.8"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

        if headers:
            request_headers.update(headers)

        request = urllib.request.Request(
            url,
            headers=request_headers,
            method="GET",
        )

        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read()

            charset = response.headers.get_content_charset()

            if charset:
                try:
                    return data.decode(charset, errors="replace")
                except (LookupError, UnicodeDecodeError):
                    pass

            return data.decode("utf-8", errors="replace")


    """
    Task 2:
    Search multiple web sources and collect readable evidence.
    This class intentionally does NOT perform AI verification.
    Verification belongs to Task 3.
    """
    SEARCH_URL = "https://html.duckduckgo.com/html/?q={}"
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/139.0.0.0 Safari/537.36"
    )
    MAX_CONTENT_LENGTH = 12000
    MAX_SNIPPET_LENGTH = 500
    MAX_FETCH_BYTES = 2_000_000

    
    def __init__(self):
        pass




    def search(self, question: str, max_sources: int = 5):
        """Search the web using multiple providers with fallbacks."""
        question = (question or "").strip()

        if not question:
            return []

        try:
            max_sources = max(1, min(int(max_sources), 10))
        except (TypeError, ValueError):
            max_sources = 5

        results = []
        seen_urls = set()
        # ------------------------------------------------------------
        # Provider 0: Google News RSS for news questions
        # ------------------------------------------------------------
        news_query = bool(re.search(
            r"\b(news|latest|breaking|headline|headlines|current events|today)\b",
            question,
            re.IGNORECASE,
        ))
        if news_query:
            try:
                google_news_url = (
                    "https://news.google.com/rss/search?q="
                    + urllib.parse.quote_plus(question)
                    + "&hl=en-US&gl=US&ceid=US:en"
                )
                google_news_xml = self._http_get(
                    google_news_url,
                    headers={
                        "User-Agent": self.USER_AGENT,
                        "Accept": "application/rss+xml, application/xml, text/xml",
                    },
                )
                item_pattern = re.compile(
                    r"<item\b[^>]*>(.*?)</item>",
                    re.IGNORECASE | re.DOTALL,
                )
                title_pattern = re.compile(
                    r"<title\b[^>]*>(.*?)</title>",
                    re.IGNORECASE | re.DOTALL,
                )
                link_pattern = re.compile(
                    r"<link\b[^>]*>(.*?)</link>",
                    re.IGNORECASE | re.DOTALL,
                )
                source_pattern = re.compile(
                    r"<source\b[^>]*url=[\"']([^\"']+)[\"'][^>]*>(.*?)</source>",
                    re.IGNORECASE | re.DOTALL,
                )
                for item_xml in item_pattern.findall(google_news_xml):
                    title_match = title_pattern.search(item_xml)
                    link_match = link_pattern.search(item_xml)
                    source_match = source_pattern.search(item_xml)
                    if not title_match or not link_match:
                        continue
                    title = self._repair_mojibake(
                        self._strip_html(html.unescape(title_match.group(1)))
                    ).strip()
                    article_url = html.unescape(link_match.group(1)).strip()
                    publisher_url = ""
                    publisher_name = ""
                    if source_match:
                        publisher_url = html.unescape(source_match.group(1)).strip()
                        publisher_name = self._repair_mojibake(
                            self._strip_html(html.unescape(source_match.group(2)))
                        ).strip()
                    normalized = self._normalize_url(article_url)
                    if not normalized or normalized in seen_urls:
                        continue
                    reliability_score, reliability_level = _get_source_reliability(
                        publisher_url or normalized
                    )
                    results.append(
                        WebEvidence(
                            title=title,
                            url=normalized,
                            snippet=publisher_name or title,
                            source=publisher_name or "Google News",
                            content="",
                            reliability_score=reliability_score,
                            reliability_level=reliability_level,
                        )
                    )
                    seen_urls.add(normalized)
                    if len(results) >= max_sources:
                        return results[:max_sources]
            except Exception:
                pass


        # ------------------------------------------------------------
        # Provider 1: DuckDuckGo HTML
        # ------------------------------------------------------------
        try:
            ddg_url = (
                "https://html.duckduckgo.com/html/?q="
                + urllib.parse.quote_plus(question)
            )

            ddg_html = self._http_get(ddg_url)

            lower_html = (ddg_html or "").lower()

            if (
                ddg_html
                and "anomaly-modal" not in lower_html
                and "challenge-form" not in lower_html
                and "unfortunately, bots use duckduckgo too" not in lower_html
            ):
                parsed = self._parse_search_results(ddg_html)

                for title, url, snippet in parsed:
                    normalized = self._normalize_url(url)

                    if not normalized or normalized in seen_urls:
                        continue

                    results.append(
                        WebEvidence(
                            title=title,
                            url=normalized,
                            snippet=snippet,
                            source="DuckDuckGo",
                            content="",
                        )
                    )

                    seen_urls.add(normalized)

                    if len(results) >= max_sources:
                        return results[:max_sources]

        except Exception:
            pass

        # ------------------------------------------------------------
        # Provider 2: Bing RSS
        # ------------------------------------------------------------
        try:
            news_query = bool(re.search(r'\b(news|latest|breaking|headline|headlines|current events|today)\b', question, re.IGNORECASE))
            bing_base = 'https://www.bing.com/news/search?format=rss&q=' if news_query else 'https://www.bing.com/search?format=rss&q='
            bing_url = bing_base + urllib.parse.quote_plus(question)

            bing_xml = self._http_get(
                bing_url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/131.0.0.0 Safari/537.36"
                    ),
                    "Accept": "application/rss+xml, application/xml, text/xml",
                },
            )

            bing_results = self._parse_bing_results(bing_xml)

            for title, url, snippet in bing_results:
                normalized = self._normalize_url(url)

                if not normalized or normalized in seen_urls:
                    continue

                results.append(
                    WebEvidence(
                        title=title,
                        url=normalized,
                        snippet=snippet,
                        source="Bing",
                        content="",
                    )
                )

                seen_urls.add(normalized)

                if len(results) >= max_sources:
                    break

        except Exception:
            pass

        return results[:max_sources]



    def _parse_bing_results(self, xml_text: str):
        """Parse Bing RSS search results."""
        results = []

        if not xml_text:
            return results

        item_pattern = re.compile(
            r"<item\b[^>]*>(.*?)</item>",
            re.IGNORECASE | re.DOTALL,
        )

        title_pattern = re.compile(
            r"<title\b[^>]*>(.*?)</title>",
            re.IGNORECASE | re.DOTALL,
        )

        link_pattern = re.compile(
            r"<link\b[^>]*>(.*?)</link>",
            re.IGNORECASE | re.DOTALL,
        )

        description_pattern = re.compile(
            r"<description\b[^>]*>(.*?)</description>",
            re.IGNORECASE | re.DOTALL,
        )

        seen = set()

        for item in item_pattern.findall(xml_text):
            title_match = title_pattern.search(item)
            link_match = link_pattern.search(item)
            description_match = description_pattern.search(item)

            if not title_match or not link_match:
                continue

            title = html.unescape(title_match.group(1)).strip()
            url = html.unescape(link_match.group(1)).strip()

            snippet = ""
            if description_match:
                snippet = html.unescape(
                    description_match.group(1)
                ).strip()

            title = self._strip_html(title)
            snippet = self._strip_html(snippet)

            title = self._repair_mojibake(title).strip()
            snippet = self._repair_mojibake(snippet).strip()

            if not title or not url:
                continue

            if not url.startswith(("http://", "https://")):
                continue

            normalized = self._normalize_url(url)

            if not normalized or normalized in seen:
                continue

            seen.add(normalized)

            results.append(
                (
                    title[:300],
                    normalized,
                    snippet[:1000],
                )
            )

        return results



    
    def collect_evidence(
        self,
        question: str,
        max_sources: int = 5,
    ) -> List[WebEvidence]:
        question = (question or "").strip()
        if not question:
            return []
        structured_weather = self._structured_weather(question)
        if structured_weather is not None:
            return [structured_weather]
        results = self.search(question, max_sources=max_sources)
        collected: List[WebEvidence] = []
        for item in results:
            content = ""
            try:
                content = self._fetch_page(item.url)
            except Exception:
                content = ""
            if content:
                content = self._clean_content_for_question(
                    content,
                    question,
                )
            if not content:
                content = item.snippet
            snippet = self._build_snippet(
                content or item.snippet,
                question,
            )
            reliability_score = item.reliability_score
            reliability_level = item.reliability_level
            

            collected.append(
                WebEvidence(
                    title=item.title,
                    url=item.url,
                    source=item.source,
                    snippet=snippet,
                    content=content[: self.MAX_CONTENT_LENGTH],
                    reliability_score=reliability_score,
                    reliability_level=reliability_level,
                )
            )

        return _verify_evidence_agreement(collected)

    
    def research(
        self,
        question: str,
        max_sources: int = 5,
    ) -> List[WebEvidence]:
        """
        Public convenience method used by the API layer.
        """
        return self.collect_evidence(
            question,
            max_sources=max_sources,
        )


    
    def _parse_search_results(self, html_text: str):
        """
        Extract DuckDuckGo HTML results robustly.
        Handles:
        - different HTML attribute orders
        - relative DuckDuckGo redirect URLs
        - absolute result URLs
        - result snippets
        """
        results = []
        if not html_text:
            return results
        # Match every anchor first instead of assuming a fixed
        # attribute order such as class -> href.
        anchor_pattern = re.compile(
            r"<a\b([^>]*)>(.*?)</a\s*>",
            re.IGNORECASE | re.DOTALL,
        )
        for match in anchor_pattern.finditer(html_text):
            attrs = match.group(1)
            inner_html = match.group(2)
            class_match = re.search(
                r'\bclass\s*=\s*["\']([^"\']*)["\']',
                attrs,
                re.IGNORECASE,
            )
            if not class_match:
                continue
            classes = class_match.group(1).lower()
            if "result__a" not in classes:
                continue
            href_match = re.search(
                r'\bhref\s*=\s*["\']([^"\']+)["\']',
                attrs,
                re.IGNORECASE,
            )
            if not href_match:
                continue
            raw_url = html.unescape(
                href_match.group(1)
            ).strip()
            title = self._strip_html(inner_html)
            title = self._repair_mojibake(title)
            if not title or len(title) < 3:
                continue
            # Convert DuckDuckGo relative redirect links into
            # their actual destination URL.
            result_url = self._normalize_search_result_url(raw_url)
            if not result_url:
                continue
            # Search nearby HTML for the corresponding snippet.
            snippet = ""
            block_start = match.start()
            block_end = min(
                len(html_text),
                match.end() + 5000,
            )
            block = html_text[block_start:block_end]
            snippet_patterns = [
                r'class=["\'][^"\']*result__snippet[^"\']*["\'][^>]*>'
                r'(.*?)</(?:a|div|span|td)>',
                r'class=["\'][^"\']*result__snippet[^"\']*["\'][^>]*>'
                r'(.*?)(?:</div>|</span>|</td>)',
            ]
            for snippet_pattern in snippet_patterns:
                snippet_match = re.search(
                    snippet_pattern,
                    block,
                    re.IGNORECASE | re.DOTALL,
                )
                if snippet_match:
                    snippet = self._strip_html(
                        snippet_match.group(1)
                    )
                    snippet = self._repair_mojibake(
                        snippet
                    )
                    if snippet:
                        break
            results.append(
                (
                    title,
                    result_url,
                    snippet,
                )
            )
        # Remove duplicate URLs while preserving order.
        unique = []
        seen = set()
        for title, url, snippet in results:
            key = self._normalize_url(url)
            if not key or key in seen:
                continue
            seen.add(key)
            unique.append(
                (
                    title,
                    key,
                    snippet,
                )
            )
        return unique

    
    def _normalize_search_result_url(self, url: str) -> str:
        """
        Convert DuckDuckGo result/redirect URLs into a normal
        absolute HTTP(S) URL.
        """
        if not url:
            return ""
        url = html.unescape(url).strip()
        # Relative DuckDuckGo redirect, e.g.
        # /l/?uddg=https%3A%2F%2Fexample.com
        if url.startswith("/"):
            url = urllib.parse.urljoin(
                "https://html.duckduckgo.com",
                url,
            )
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return ""
        host = parsed.netloc.lower()
        # DuckDuckGo redirect URL.
        if (
            "duckduckgo.com" in host
            or host.endswith("duck.com")
        ):
            query = urllib.parse.parse_qs(
                parsed.query
            )
            target = query.get("uddg")
            if target:
                target_url = html.unescape(
                    target[0]
                ).strip()
                target_parsed = urllib.parse.urlparse(
                    target_url
                )
                if target_parsed.scheme in {
                    "http",
                    "https",
                }:
                    return self._normalize_url(
                        target_url
                    )
        return self._normalize_url(url)

        
    @staticmethod
    def _weather_code_description(code) -> Optional[str]:
        """Convert WMO weather code to a human-readable condition."""
        try:
            code = int(code)
        except (TypeError, ValueError):
            return None
        descriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",
        }
        return descriptions.get(code)
    def _structured_weather(self, question: str) -> Optional[WebEvidence]:
        """Fetch structured current weather without HTML scraping."""
        question = (question or "").strip()
        if not question:
            return None
        location_match = re.search(
            r"\b(?:in|at|for)\s+([A-Za-z][A-Za-z .,'-]{1,80}?)(?:\s+(?:now|today|tonight|currently|current)\b|\?|$)",
            question,
            re.IGNORECASE,
        )
        if not location_match:
            return None
        location = location_match.group(1).strip(" .,")
        if not location:
            return None
        try:
            geocode_url = (
                "https://geocoding-api.open-meteo.com/v1/search?"
                + urllib.parse.urlencode({
                    "name": location,
                    "count": 1,
                    "language": "en",
                    "format": "json",
                })
            )
            request = urllib.request.Request(
                geocode_url,
                headers={"User-Agent": self.USER_AGENT},
                method="GET",
            )
            with urllib.request.urlopen(request, timeout=15) as response:
                geo_data = json.loads(
                    response.read().decode("utf-8")
                )
            results = geo_data.get("results") or []
            if not results:
                return None
            place = results[0]
            latitude = place.get("latitude")
            longitude = place.get("longitude")
            place_name = str(place.get("name") or location).strip()
            country = str(place.get("country") or "").strip()
            if latitude is None or longitude is None:
                return None
            forecast_url = (
                "https://api.open-meteo.com/v1/forecast?"
                + urllib.parse.urlencode({
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": (
                        "temperature_2m,"
                        "relative_humidity_2m,"
                        "apparent_temperature,"
                        "precipitation,"
                        "rain,"
                        "showers,"
                        "snowfall,"
                        "weather_code,"
                        "wind_speed_10m"
                    ),
                    "timezone": "auto",
                })
            )
            request = urllib.request.Request(
                forecast_url,
                headers={"User-Agent": self.USER_AGENT},
                method="GET",
            )
            with urllib.request.urlopen(request, timeout=15) as response:
                weather_data = json.loads(
                    response.read().decode("utf-8")
                )
            current = weather_data.get("current") or {}
            if not current:
                return None
            units = weather_data.get("current_units") or {}
            temperature = current.get("temperature_2m")
            apparent = current.get("apparent_temperature")
            humidity = current.get("relative_humidity_2m")
            precipitation = current.get("precipitation")
            rain = current.get("rain")
            showers = current.get("showers")
            snowfall = current.get("snowfall")
            wind = current.get("wind_speed_10m")
            weather_code = current.get("weather_code")
            observed_time = current.get("time")
            details = [
                f"Location: {place_name}"
                + (f", {country}" if country else ""),
                f"Observation time: {observed_time}",
            ]
            if temperature is not None:
                details.append(
                    f"Temperature: {temperature} "
                    f"{units.get('temperature_2m', '?C')}"
                )
            if apparent is not None:
                details.append(
                    f"Feels like: {apparent} "
                    f"{units.get('apparent_temperature', '?C')}"
                )
            if humidity is not None:
                details.append(
                    f"Relative humidity: {humidity} "
                    f"{units.get('relative_humidity_2m', '%')}"
                )
            if precipitation is not None:
                details.append(
                    f"Precipitation: {precipitation} "
                    f"{units.get('precipitation', 'mm')}"
                )
            if rain is not None:
                details.append(
                    f"Rain: {rain} "
                    f"{units.get('rain', 'mm')}"
                )
            if showers is not None:
                details.append(
                    f"Showers: {showers} "
                    f"{units.get('showers', 'mm')}"
                )
            if snowfall is not None:
                details.append(
                    f"Snowfall: {snowfall} "
                    f"{units.get('snowfall', 'cm')}"
                )
            if wind is not None:
                details.append(
                    f"Wind speed: {wind} "
                    f"{units.get('wind_speed_10m', 'km/h')}"
                )
            if weather_code is not None:
                details.append(
                    f"Weather code: {weather_code}"
                )
                condition = self._weather_code_description(weather_code)
                if condition:
                    details.append(
                        f"Weather condition: {condition}"
                    )
            content = "\n".join(details)
            return WebEvidence(
                title=f"Current Weather ? {place_name}",
                url=forecast_url,
                source="Open-Meteo",
                snippet=content[: self.MAX_SNIPPET_LENGTH],
                content=content,
                reliability_score=0.75,
                reliability_level="medium",
                verification_status="verified",
            )
        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            json.JSONDecodeError,
            TimeoutError,
            ValueError,
            TypeError,
        ):
            return None
    def _fetch_page(self, url: str) -> str:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": self.USER_AGENT,
                "Accept": (
                    "text/html,application/xhtml+xml,"
                    "application/xml;q=0.9,text/plain;q=0.8,*/*;q=0.5"
                ),
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "close",
            },
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            data = response.read(self.MAX_FETCH_BYTES)
            content_type = response.headers.get("Content-Type", "")
            encoding = response.headers.get_content_charset()
            content_encoding = (
                response.headers.get("Content-Encoding", "") or ""
            ).lower()
        if content_encoding == "gzip":
            try:
                data = gzip.decompress(data)
            except Exception:
                pass
        elif content_encoding == "deflate":
            try:
                data = zlib.decompress(data)
            except Exception:
                pass
        if "text/html" not in content_type.lower() and not self._looks_like_html(data):
            text = self._decode_bytes(data, encoding)
            return self._clean_text(text)[: self.MAX_CONTENT_LENGTH]
        text = self._decode_bytes(data, encoding)
        parser = _HTMLTextParser()
        try:
            parser.feed(text)
            parser.close()
            extracted = parser.get_text()
        except Exception:
            extracted = self._fallback_clean_html(text)
        extracted = self._repair_mojibake(extracted)
        extracted = html.unescape(extracted)
        extracted = self._normalize_extracted_text(extracted)
        return extracted[: self.MAX_CONTENT_LENGTH]


    
    def _clean_content_for_question(
        self,
        content: str,
        question: str,
    ) -> str:
        content = self._normalize_extracted_text(content)
        if not content:
            return ""
        # Split into useful blocks.
        blocks = [
            self._clean_text(block)
            for block in re.split(r"\n+", content)
        ]
        blocks = [
            block
            for block in blocks
            if self._is_useful_block(block)
        ]
        if not blocks:
            return ""
        question_words = self._keywords(question)
        scored = []
        for index, block in enumerate(blocks):
            words = self._keywords(block)
            overlap = len(question_words.intersection(words))
            # Prefer explanatory text over tiny UI fragments.
            length_bonus = min(len(block) / 250.0, 2.0)
            # Headings and early article blocks often contain useful context.
            position_bonus = max(0.0, 1.0 - index / 40.0)
            score = overlap * 3.0 + length_bonus + position_bonus
            scored.append((score, index, block))
        # Keep natural page order while prioritizing relevant blocks.
        relevant = [
            item
            for item in scored
            if item[0] >= 2.0
        ]
        if relevant:
            selected_indices = {
                index
                for _, index, _ in sorted(
                    relevant,
                    key=lambda x: x[0],
                    reverse=True,
                )[:18]
            }
            selected = [
                block
                for index, block in enumerate(blocks)
                if index in selected_indices
            ]
        else:
            selected = blocks[:18]
        result = "\n".join(selected)
        result = self._remove_repeated_noise(result)
        result = self._normalize_extracted_text(result)
        return result[: self.MAX_CONTENT_LENGTH]


    
    def _is_useful_block(self, block: str) -> bool:
        block = self._clean_text(block)
        if not block:
            return False
        if len(block) < 25:
            # Keep meaningful headings.
            if len(block.split()) >= 3:
                return True
            return False
        if len(block) > 1000:
            # Large blocks are usually mixed navigation/content.
            return True
        words = block.split()
        if len(words) < 4:
            return False
        lower = block.lower()
        noise_phrases = (
            "skip to content",
            "sign in",
            "log in",
            "create account",
            "all rights reserved",
            "privacy policy",
            "terms of service",
            "cookie settings",
            "accept cookies",
            "subscribe to our newsletter",
        )
        if any(phrase in lower for phrase in noise_phrases):
            return False
        # Reject obvious menu-like blocks.
        if len(words) <= 15:
            menu_words = {
                "home",
                "about",
                "contact",
                "login",
                "search",
                "menu",
                "pricing",
                "careers",
                "privacy",
                "terms",
            }
            if len(set(word.lower() for word in words) & menu_words) >= 3:
                return False
        return True


    
    def _remove_repeated_noise(self, text: str) -> str:
        lines = [
            self._clean_text(line)
            for line in text.splitlines()
        ]
        counts = {}
        for line in lines:
            if 10 <= len(line) <= 250:
                key = re.sub(r"\s+", " ", line.lower())
                counts[key] = counts.get(key, 0) + 1
        output = []
        for line in lines:
            if not line:
                continue
            key = re.sub(r"\s+", " ", line.lower())
            # Repeated navigation labels are rarely evidence.
            if counts.get(key, 0) >= 4 and len(line.split()) <= 12:
                continue
            output.append(line)
        return "\n".join(output)


    
    def _build_snippet(
        self,
        content: str,
        question: str,
    ) -> str:
        content = self._clean_text(content)
        if not content:
            return ""
        question_words = self._keywords(question)
        sentences = re.split(
            r"(?<=[.!?])\s+",
            content,
        )
        scored = []
        for index, sentence in enumerate(sentences):
            sentence = self._clean_text(sentence)
            if not sentence:
                continue
            words = self._keywords(sentence)
            overlap = len(question_words.intersection(words))
            score = overlap * 5
            if 50 <= len(sentence) <= 300:
                score += 1
            scored.append((score, -index, sentence))
        if scored:
            scored.sort(reverse=True)
            best = scored[0][2]
            if len(best) < 80 and len(sentences) > 1:
                for sentence in sentences:
                    if sentence != best and len(sentence) > 50:
                        best = best + " " + sentence
                        break
            return best[: self.MAX_SNIPPET_LENGTH].strip()
        return content[: self.MAX_SNIPPET_LENGTH].strip()


    
    def _keywords(self, text: str):
        words = re.findall(
            r"[A-Za-z0-9]+",
            (text or "").lower(),
        )
        stopwords = {
            "what",
            "is",
            "are",
            "the",
            "a",
            "an",
            "of",
            "to",
            "in",
            "on",
            "for",
            "and",
            "or",
            "how",
            "why",
            "when",
            "where",
            "who",
            "which",
            "does",
            "do",
            "can",
            "please",
            "tell",
            "me",
            "latest",
            "current",
            "information",
            "about",
        }
        return {
            word
            for word in words
            if len(word) >= 3 and word not in stopwords
        }


    
    def _fallback_clean_html(self, text: str) -> str:
        text = re.sub(
            r"<(script|style|noscript|svg|template|nav|header|footer|aside|form|iframe|canvas)"
            r"\b[^>]*>.*?</\1\s*>",
            " ",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        text = re.sub(r"<[^>]+>", "\n", text)
        return self._clean_text(html.unescape(text))

    
    def _normalize_extracted_text(self, text: str) -> str:
        text = html.unescape(text)
        text = self._repair_mojibake(text)
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")
        text = text.replace("\xa0", " ")
        # Remove zero-width/control characters.
        text = re.sub(
            r"[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]",
            " ",
            text,
        )
        # Normalize excessive whitespace without destroying paragraphs.
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n[ \t]+", "\n", text)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    
    def _clean_text(self, value: str) -> str:
        if not value:
            return ""
        value = html.unescape(value)
        # If raw HTML is still present.
        if "<" in value and ">" in value:
            value = self._strip_html(value)
        value = self._repair_mojibake(value)
        value = re.sub(
            r"[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]",
            " ",
            value,
        )
        value = re.sub(r"\s+", " ", value)
        return value.strip()

    
    def _strip_html(self, value: str) -> str:
        parser = _HTMLTextParser()
        try:
            parser.feed(value)
            parser.close()
            result = parser.get_text()
        except Exception:
            result = re.sub(r"<[^>]+>", " ", value)
        return self._normalize_extracted_text(result)

    
    def _decode_bytes(
        self,
        data: bytes,
        declared_encoding: Optional[str] = None,
    ) -> str:
        encodings = []
        if declared_encoding:
            encodings.append(declared_encoding)
        # BOMs.
        if data.startswith(b"\xef\xbb\xbf"):
            encodings.insert(0, "utf-8-sig")
        elif data.startswith(b"\xff\xfe"):
            encodings.insert(0, "utf-16")
        elif data.startswith(b"\xfe\xff"):
            encodings.insert(0, "utf-16-be")
        encodings.extend(
            [
                "utf-8",
                "cp1252",
                "latin-1",
            ]
        )
        tried = set()
        for encoding in encodings:
            encoding = encoding.lower()
            if encoding in tried:
                continue
            tried.add(encoding)
            try:
                return data.decode(encoding)
            except (UnicodeDecodeError, LookupError):
                continue
        return data.decode("utf-8", errors="replace")

    
    def _repair_mojibake(self, value: str) -> str:
        """
        Safely repair common UTF-8-as-CP1252/Latin-1 mojibake.
        This intentionally does NOT treat ordinary characters such as
        é, ©, ° etc. as mojibake markers because those are valid Unicode.
        """
        if not value:
            return value
        current = value
        for _ in range(2):
            if not self._looks_mojibake(current):
                break
            candidates = [current]
            for encoding in ("cp1252", "latin-1"):
                try:
                    candidate = current.encode(encoding).decode(
                        "utf-8",
                        errors="strict",
                    )
                    candidates.append(candidate)
                except (UnicodeEncodeError, UnicodeDecodeError):
                    continue
            best = min(
                candidates,
                key=self._mojibake_score,
            )
            if best == current:
                break
            current = best
        # Common remaining broken punctuation sequences.
        replacements = {
            "â€™": "’",
            "â€˜": "‘",
            "â€œ": "“",
            "â€\x9d": "”",
            "â€“": "–",
            "â€”": "—",
            "â€¦": "…",
            "Â©": "©",
            "Â®": "®",
            "Â°": "°",
            "Â±": "±",
            "Â·": "·",
            "Â ": " ",
        }
        for old, new in replacements.items():
            current = current.replace(old, new)
        return current

    
    def _looks_mojibake(self, value: str) -> bool:
        patterns = (
            r"Ã[\x80-\xBF]",
            r"Â[\x80-\xBF]",
            r"â[\x80-\xBF]",
            r"ð[\x80-\xBF]",
            r"Ð[\x80-\xBF]",
            r"Ñ[\x80-\xBF]",
            r"[\u0080-\u009F]",
        )
        return any(re.search(pattern, value) for pattern in patterns)


    
    def _mojibake_score(self, value: str) -> int:
        score = 0
        bad_patterns = (
            r"Ã[\x80-\xBF]",
            r"Â[\x80-\xBF]",
            r"â[\x80-\xBF]",
            r"ð[\x80-\xBF]",
            r"Ð[\x80-\xBF]",
            r"Ñ[\x80-\xBF]",
            r"[\u0080-\u009F]",
        )
        for pattern in bad_patterns:
            score += len(re.findall(pattern, value))
        # Common visibly broken sequences.
        score += value.count("â€™") * 3
        score += value.count("â€œ") * 3
        score += value.count("â€") * 2
        score += value.count("Â ") * 2
        return score

    
    def _looks_like_html(self, data: bytes) -> bool:
        sample = data[:4000].lower()
        return (
            b"<html" in sample
            or b"<!doctype html" in sample
            or b"<body" in sample
            or b"<article" in sample
        )


    
    def _normalize_url(self, url: str) -> str:
        if not url:
            return ""
        url = html.unescape(url).strip()
        # DuckDuckGo may return redirect URLs.
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return ""
        query = urllib.parse.parse_qs(parsed.query)
        if parsed.netloc.lower().endswith("duckduckgo.com"):
            target = query.get("uddg")
            if target:
                candidate = target[0]
                if candidate.startswith(("http://", "https://")):
                    url = candidate
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return ""
        # Remove fragments; they don't identify a different source page.
        parsed = parsed._replace(fragment="")
        return urllib.parse.urlunparse(parsed)

    
    def _detect_charset(self, text: str) -> Optional[str]:
        match = re.search(
            r'<meta[^>]+charset=["\']?\s*([a-zA-Z0-9._-]+)',
            text,
            flags=re.IGNORECASE,
        )
        if match:
            return match.group(1)
        match = re.search(
            r'<meta[^>]+content=["\'][^"\']*charset=([a-zA-Z0-9._-]+)',
            text,
            flags=re.IGNORECASE,
        )
        if match:
            return match.group(1)
        return None







