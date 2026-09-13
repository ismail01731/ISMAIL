"""
ISMAIL AI - News Filtering

Keeps irrelevant / noisy results out of broad
current-events searches.

This module only filters.
It does not perform web searches or verification.
"""

import re


def is_bad_broad_current_event_result(
    title: str,
    url: str,
    snippet: str,
    broad_current_events: bool,
) -> bool:
    """
    Return True when a search result is clearly unsuitable
    for a broad current-events query.
    """

    if not broad_current_events:
        return False

    text = f"{title or ''} {url or ''} {snippet or ''}".lower()

    # ---------------------------------------------------------
    # Historical / anniversary noise
    # ---------------------------------------------------------
    historical_patterns = [
        r"\b9\s*[/\-·]\s*11\b",
        r"\bseptember\s+11\b",
        r"\bsept\.?\s+11\b",
        r"\bseptember\s+11\b",
        r"\b11\s+september\b",
        r"৯/১১",
        r"বার্ষিকী",
        r"\banniversary\b",
        r"\bremembrance\b",
        r"\bremembering\b",
        r"\b25th\s+anniversary\b",
    ]

    if any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in historical_patterns
    ):
        return True

    # ---------------------------------------------------------
    # Generic news pages instead of actual events
    # ---------------------------------------------------------
    generic_news_patterns = [
        r"\bnews homepage\b",
        r"\bnews home\b",
        r"\btop headlines\b",
        r"\bheadlines\b",
        r"\blatest news\b",
        r"\bworld news\b",
        r"\binternational news\b",
        r"\blatest world news\b",
        r"\binternational headlines\b",
        r"\bworld headlines\b",
        r"\blive updates\b",
        r"\b24/7 news\b",
        r"\bnews 24/7\b",
        r"\bnews videos?\b",
        r"\bnews videos? photos\b",
        r"news\.un\.org/en/?$",
        r"\bglobal perspective human stories\b",
        r"即时新闻",
        r"国际要闻",
        r"新华国际",
    ]

    if any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in generic_news_patterns
    ):
        return True

    # ---------------------------------------------------------
    # Social media / video results
    # ---------------------------------------------------------
    social_patterns = [
        r"youtube\.com",
        r"youtu\.be",
        r"facebook\.com",
        r"instagram\.com",
        r"tiktok\.com",
    ]

    if any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in social_patterns
    ):
        return True

    # ---------------------------------------------------------
    # Search / gaming / unrelated junk
    # ---------------------------------------------------------
    junk_patterns = [
        r"microsoft community",
        r"answers\.microsoft\.com",
        r"\bcourt records\b",
        r"courtcasefinder",
        r"\becourt\b",
        r"\brecords search\b",
        r"\bage of empires\b",
        r"\bwalkthrough\b",
        r"\bgame guide\b",
        r"\bcheat\b",
        r"\bcheats\b",
        r"\bwhat is pi\b",
        r"\bpi equals\b",
        r"π等于多少",
        r"\byandex\b",
        r"百度知道",
        r"\bbaidu\b",
    ]

    if any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in junk_patterns
    ):
        return True

    return False


def is_bangladesh_news_result(
    title: str,
    url: str,
    snippet: str,
) -> bool:
    """
    Detect whether a result appears to be related to Bangladesh.
    """

    text = f"{title or ''} {url or ''} {snippet or ''}".lower()

    bangladesh_signals = [
        "bangladesh",
        "বাংলাদেশ",
        "dhaka",
        "ঢাকা",
        "chittagong",
        "chattogram",
        "চট্টগ্রাম",
        "sylhet",
        "সিলেট",
        "khulna",
        "খুলনা",
        "rajshahi",
        "রাজশাহী",
        "barisal",
        "বরিশাল",
        "rangpur",
        "রংপুর",
        "mymensingh",
        "ময়মনসিংহ",
    ]

    return any(
        signal in text
        for signal in bangladesh_signals
    )


def is_global_news_result(
    title: str,
    url: str,
    snippet: str,
) -> bool:
    """
    Detect whether a result appears to be a global/international
    news result rather than Bangladesh-specific content.
    """

    text = f"{title or ''} {url or ''} {snippet or ''}".lower()

    bangladesh_patterns = [
        r"\bbangladesh\b",
        r"\bdhaka\b",
        r"\bchittagong\b",
        r"\bchattogram\b",
        r"\bsylhet\b",
        r"বাংলাদেশ",
        r"ঢাকা",
        r"চট্টগ্রাম",
        r"সিলেট",
    ]

    return not any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in bangladesh_patterns
    )




def is_relevant_broad_current_event(
    title: str,
    url: str,
    snippet: str,
) -> bool:
    """
    Detect whether a result looks like an actual current event
    rather than an unrelated article.
    """

    text = f"{title or ''} {url or ''} {snippet or ''}".lower()

    # ---------------------------------------------------------
    # Clearly unrelated / non-event topics
    # ---------------------------------------------------------
    unrelated_patterns = [
        r"\brecord winter\b",
        r"\bmountain of snow\b",
        r"\bweather\b",
        r"\bforecast\b",
        r"\bhoroscope\b",
        r"\brecipe\b",
        r"\bcooking\b",
        r"\bmovie review\b",
        r"\bfilm review\b",
        r"\bsports scores?\b",
        r"\bgame guide\b",
        r"\bwalkthrough\b",
        r"\bcheat\b",
        r"\bquiz\b",
        r"\bmeaning of\b",
        r"\bdefinition of\b",
        r"\bhow to\b",
        r"\btutorial\b",
    ]

    if any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in unrelated_patterns
    ):
        return False

    # Broad current-events searches should be inclusive.
    # Only clearly unrelated content is rejected.

    return True