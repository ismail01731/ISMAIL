import re
from typing import Optional
STOP_WORDS = {
    "the", "a", "an", "is", "are", "of", "to", "and", "in",
    "for", "on", "with", "this", "that", "how", "what", "why",
    "এর", "এই", "একটি", "এবং", "করা", "করার", "কি", "কী",
}
def _clean(text: str) -> str:
    return str(text or "").strip()
def _words(text: str):
    return re.findall(r"\S+", _clean(text).lower())
def _keywords(text: str):
    words = _words(text)
    result = []
    for word in words:
        word = re.sub(r"[^\w\u0980-\u09FF-]", "", word)
        if not word:
            continue
        if word in STOP_WORDS:
            continue
        if len(word) < 2:
            continue
        if word not in result:
            result.append(word)
    return result
def analyze_seo(
    title: str,
    description: str = "",
    tags: Optional[list] = None,
):
    title = _clean(title)
    description = _clean(description)
    tags = tags or []
    title_words = _keywords(title)
    description_words = _keywords(description)
    normalized_tags = [
        _clean(tag).lower()
        for tag in tags
        if _clean(tag)
    ]
    score = 50
    title_length = len(title)
    description_length = len(description)
    if 30 <= title_length <= 70:
        score += 15
    elif 20 <= title_length <= 90:
        score += 8
    elif title_length > 100:
        score -= 10
    if 80 <= description_length <= 5000:
        score += 10
    elif description_length > 0:
        score += 4
    if normalized_tags:
        score += min(len(normalized_tags) * 2, 10)
    keyword_overlap = set(title_words) & set(description_words)
    if keyword_overlap:
        score += min(len(keyword_overlap) * 3, 10)
    if "#" in description:
        score += 3
    if "subscribe" in description.lower() or "সাবস্ক্রাইব" in description:
        score += 2
    if "like" in description.lower() or "লাইক" in description:
        score += 2
    score = max(0, min(100, score))
    recommendations = []
    if title_length < 30:
        recommendations.append(
            "Title আরও descriptive করুন এবং মূল keyword যোগ করুন।"
        )
    if title_length > 90:
        recommendations.append(
            "Title ছোট করুন যাতে মূল বিষয়টি দ্রুত বোঝা যায়।"
        )
    if description_length < 80:
        recommendations.append(
            "Description-এ ভিডিওর বিষয়, context এবং relevant keywords যোগ করুন।"
        )
    if not normalized_tags:
        recommendations.append(
            "Relevant search tags যোগ করুন।"
        )
    if not keyword_overlap and title_words:
        recommendations.append(
            "Title-এর গুরুত্বপূর্ণ keywords description-এ naturally ব্যবহার করুন।"
        )
    return {
        "success": True,
        "title": title,
        "description": description,
        "tags": normalized_tags,
        "seo_score": score,
        "title_length": title_length,
        "description_length": description_length,
        "title_keywords": title_words,
        "description_keywords": description_words,
        "keyword_overlap": sorted(keyword_overlap),
        "recommendations": recommendations,
    }
def generate_description(
    title: str,
    topic: str,
    channel_name: str = "The Ismail Jr",
):
    title = _clean(title)
    topic = _clean(topic)
    channel_name = _clean(channel_name) or "The Ismail Jr"
    description = (
        f"{title}\n\n"
        f"আজকের ভিডিওতে আমরা {topic} নিয়ে একটি মজার ও entertaining ভিডিও করেছি। "
        f"ভিডিওটি শেষ পর্যন্ত দেখুন এবং আপনার মতামত কমেন্টে জানান।\n\n"
        f"👍 ভালো লাগলে Like করুন\n"
        f"🔔 নতুন ভিডিও পেতে Subscribe করুন\n"
        f"💬 আপনার মতামত Comment করুন\n\n"
        f"Channel: {channel_name}\n\n"
        f"#Shorts #BanglaComedy #VillageVlog"
    )
    return {
        "success": True,
        "title": title,
        "topic": topic,
        "channel_name": channel_name,
        "description": description,
    }
def generate_tags(
    title: str,
    topic: str,
    language: str = "bn",
    count: int = 20,
):
    title = _clean(title)
    topic = _clean(topic)
    source_words = _keywords(
        f"{title} {topic}"
    )
    tags = []
    for word in source_words:
        if word not in tags:
            tags.append(word)
    templates = [
        topic,
        f"{topic} বাংলা",
        f"{topic} Bangla",
        f"{topic} comedy",
        f"{topic} funny",
        f"{topic} shorts",
        f"{topic} short video",
        "Bangla comedy",
        "Bangla funny video",
        "Bangla shorts",
        "Village comedy",
        "Village vlog",
        "Bangladesh comedy",
        "বাংলা কমেডি",
        "বাংলা শর্টস",
        "গ্রামের ভিডিও",
        "মজার ভিডিও",
        "funny shorts",
        "comedy shorts",
    ]
    if language.lower() == "bn":
        templates.extend([
            f"{topic} বাংলা ভিডিও",
            f"{topic} মজার ভিডিও",
        ])
    for tag in templates:
        tag = _clean(tag).lower()
        if tag and tag not in tags:
            tags.append(tag)
    count = max(1, min(int(count), 50))
    return {
        "success": True,
        "title": title,
        "topic": topic,
        "language": language,
        "tags": tags[:count],
        "tag_string": ", ".join(tags[:count]),
    }
def generate_hashtags(
    title: str,
    topic: str,
    count: int = 8,
):
    title = _clean(title)
    topic = _clean(topic)
    candidates = [
        "#Shorts",
        "#BanglaComedy",
        "#BanglaShorts",
        "#VillageVlog",
        "#FunnyVideo",
        "#Comedy",
        "#Bangladesh",
        "#গ্রামেরভিডিও",
        "#বাংলাকমেডি",
        "#মজারভিডিও",
        f"#{re.sub(r'[^A-Za-z0-9\u0980-\u09FF]', '', topic)}",
    ]
    result = []
    for hashtag in candidates:
        if hashtag not in result and len(hashtag) > 1:
            result.append(hashtag)
    count = max(1, min(int(count), 15))
    return {
        "success": True,
        "title": title,
        "topic": topic,
        "hashtags": result[:count],
        "hashtag_string": " ".join(result[:count]),
    }
def build_seo_package(
    title: str,
    topic: str,
    channel_name: str = "The Ismail Jr",
    language: str = "bn",
):
    description_result = generate_description(
        title,
        topic,
        channel_name,
    )
    tags_result = generate_tags(
        title,
        topic,
        language,
        20,
    )
    hashtag_result = generate_hashtags(
        title,
        topic,
        8,
    )
    analysis = analyze_seo(
        title,
        description_result["description"],
        tags_result["tags"],
    )
    return {
        "success": True,
        "title": title,
        "topic": topic,
        "channel_name": channel_name,
        "language": language,
        "seo_score": analysis["seo_score"],
        "description": description_result["description"],
        "tags": tags_result["tags"],
        "tag_string": tags_result["tag_string"],
        "hashtags": hashtag_result["hashtags"],
        "hashtag_string": hashtag_result["hashtag_string"],
        "analysis": analysis,
    }
class YouTubeSEOEngine:
    def analyze(
        self,
        title: str,
        description: str = "",
        tags: Optional[list] = None,
    ):
        return analyze_seo(title, description, tags)
    def description(
        self,
        title: str,
        topic: str,
        channel_name: str = "The Ismail Jr",
    ):
        return generate_description(title, topic, channel_name)
    def tags(
        self,
        title: str,
        topic: str,
        language: str = "bn",
        count: int = 20,
    ):
        return generate_tags(title, topic, language, count)
    def hashtags(
        self,
        title: str,
        topic: str,
        count: int = 8,
    ):
        return generate_hashtags(title, topic, count)
    def package(
        self,
        title: str,
        topic: str,
        channel_name: str = "The Ismail Jr",
        language: str = "bn",
    ):
        return build_seo_package(
            title,
            topic,
            channel_name,
            language,
        )
seo_engine = YouTubeSEOEngine()
