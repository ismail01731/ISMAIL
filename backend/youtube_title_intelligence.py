import sqlite3
import re
from pathlib import Path
from typing import Optional
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "youtube_growth.db"
def _connect():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn
def _avg(values):
    values = [float(v) for v in values if v is not None]
    return round(sum(values) / len(values), 2) if values else 0.0
def _title_features(title: str):
    title = str(title or "").strip()
    words = re.findall(r"\S+", title)
    word_count = len(words)
    question = "?" in title
    exclamation = "!" in title
    emoji = bool(re.search(r"[^\x00-\x7F]", title))
    number = bool(re.search(r"\d", title))
    curiosity_words = {
        "কিভাবে", "কেন", "কি", "সত্যি", "রহস্য", "দেখুন",
        "জানুন", "সেরা", "শেষে", "অবশেষে", "চমক",
        "how", "why", "what", "secret", "best", "finally",
        "truth", "watch", "revealed"
    }
    curiosity = sum(
        1 for word in words
        if word.strip(".,!?()[]{}\"'").lower() in curiosity_words
    )
    return {
        "title_length": len(title),
        "word_count": word_count,
        "has_question": question,
        "has_exclamation": exclamation,
        "has_emoji": emoji,
        "has_number": number,
        "curiosity_word_count": curiosity,
    }
def analyze_title(title: str):
    features = _title_features(title)
    score = 50.0
    if 25 <= features["title_length"] <= 65:
        score += 10
    if 4 <= features["word_count"] <= 12:
        score += 10
    if features["has_question"]:
        score += 5
    if features["has_exclamation"]:
        score += 4
    if features["has_number"]:
        score += 4
    if features["has_emoji"]:
        score += 3
    if features["curiosity_word_count"] > 0:
        score += min(features["curiosity_word_count"] * 5, 10)
    if features["title_length"] > 90:
        score -= 12
    if features["word_count"] > 18:
        score -= 8
    score = round(min(max(score, 0), 100), 2)
    return {
        "success": True,
        "title": title,
        "title_score": score,
        "features": features,
    }
def analyze_channel_titles(
    channel_id: Optional[str] = None,
    limit: int = 100,
):
    limit = max(1, min(int(limit or 100), 1000))
    with _connect() as conn:
        if channel_id:
            channel = conn.execute(
                """
                SELECT *
                FROM youtube_channels
                WHERE channel_id = ?
                """,
                (channel_id,),
            ).fetchone()
            if not channel:
                raise ValueError("YouTube channel not found")
            videos = conn.execute(
                """
                SELECT
                    youtube_video_id,
                    title,
                    topic,
                    format,
                    views,
                    likes,
                    comments,
                    ctr,
                    average_percentage_viewed
                FROM youtube_videos
                WHERE channel_id = ?
                ORDER BY views DESC, id DESC
                LIMIT ?
                """,
                (channel["id"], limit),
            ).fetchall()
        else:
            channel = conn.execute(
                """
                SELECT *
                FROM youtube_channels
                ORDER BY id DESC
                LIMIT 1
                """
            ).fetchone()
            if channel:
                videos = conn.execute(
                    """
                    SELECT
                        youtube_video_id,
                        title,
                        topic,
                        format,
                        views,
                        likes,
                        comments,
                        ctr,
                        average_percentage_viewed
                    FROM youtube_videos
                    WHERE channel_id = ?
                    ORDER BY views DESC, id DESC
                    LIMIT ?
                    """,
                    (channel["id"], limit),
                ).fetchall()
            else:
                videos = []
    videos = [dict(v) for v in videos]
    analyzed = []
    for video in videos:
        result = analyze_title(video.get("title") or "")
        result.update(
            {
                "youtube_video_id": video.get("youtube_video_id"),
                "topic": video.get("topic"),
                "format": video.get("format"),
                "views": int(video.get("views") or 0),
                "likes": int(video.get("likes") or 0),
                "comments": int(video.get("comments") or 0),
                "ctr": video.get("ctr"),
                "average_percentage_viewed": video.get(
                    "average_percentage_viewed"
                ),
            }
        )
        analyzed.append(result)
    if not analyzed:
        return {
            "success": True,
            "channel_id": channel["channel_id"] if channel else None,
            "channel_name": channel["channel_name"] if channel else None,
            "analyzed_video_count": 0,
            "average_title_score": 0.0,
            "average_ctr": 0.0,
            "average_views": 0.0,
            "top_titles": [],
            "title_patterns": [],
        }
    average_title_score = _avg(
        [x["title_score"] for x in analyzed]
    )
    average_ctr = _avg(
        [x.get("ctr") for x in analyzed if x.get("ctr") is not None]
    )
    average_views = _avg(
        [x.get("views") for x in analyzed]
    )
    top_titles = sorted(
        analyzed,
        key=lambda x: (
            int(x.get("views") or 0),
            float(x.get("ctr") or 0),
            x["title_score"],
        ),
        reverse=True,
    )[:10]
    patterns = {
        "question_titles": [
            x for x in analyzed
            if x["features"]["has_question"]
        ],
        "number_titles": [
            x for x in analyzed
            if x["features"]["has_number"]
        ],
        "emoji_titles": [
            x for x in analyzed
            if x["features"]["has_emoji"]
        ],
        "curiosity_titles": [
            x for x in analyzed
            if x["features"]["curiosity_word_count"] > 0
        ],
    }
    title_patterns = []
    for pattern_name, items in patterns.items():
        if not items:
            continue
        title_patterns.append(
            {
                "pattern": pattern_name,
                "video_count": len(items),
                "average_views": _avg(
                    [x.get("views") for x in items]
                ),
                "average_ctr": _avg(
                    [
                        x.get("ctr")
                        for x in items
                        if x.get("ctr") is not None
                    ]
                ),
                "average_title_score": _avg(
                    [x["title_score"] for x in items]
                ),
            }
        )
    return {
        "success": True,
        "channel_id": channel["channel_id"] if channel else None,
        "channel_name": channel["channel_name"] if channel else None,
        "analyzed_video_count": len(analyzed),
        "average_title_score": average_title_score,
        "average_ctr": average_ctr,
        "average_views": average_views,
        "top_titles": top_titles,
        "title_patterns": title_patterns,
    }
def compare_titles(
    title_a: str,
    title_b: str,
):
    a = analyze_title(title_a)
    b = analyze_title(title_b)
    difference = round(
        a["title_score"] - b["title_score"],
        2,
    )
    return {
        "success": True,
        "title_a": a,
        "title_b": b,
        "score_difference": difference,
    }
def generate_title_variants(
    base_topic: str,
    count: int = 5,
):
    base_topic = str(base_topic or "").strip()
    if not base_topic:
        raise ValueError("base_topic is required")
    count = max(1, min(int(count or 5), 10))
    templates = [
        f"{base_topic} 😂",
        f"{base_topic} — আসল ঘটনা কী?",
        f"{base_topic} এর সঠিক নিয়ম 😂",
        f"{base_topic}: শেষে যা হলো! 😱",
        f"{base_topic} Challenge 😂",
        f"কিভাবে {base_topic} করবেন? 😂",
        f"{base_topic} নিয়ে এই ভুলটা করবেন না!",
        f"{base_topic} | Funny Village Comedy",
        f"{base_topic} — শেষ পর্যন্ত দেখুন 😂",
        f"সত্যিই কি {base_topic}? 😳",
    ]
    variants = []
    for title in templates[:count]:
        result = analyze_title(title)
        variants.append(
            {
                "title": title,
                "title_score": result["title_score"],
                "features": result["features"],
            }
        )
    variants.sort(
        key=lambda x: x["title_score"],
        reverse=True,
    )
    return {
        "success": True,
        "base_topic": base_topic,
        "count": len(variants),
        "variants": variants,
    }
class YouTubeTitleIntelligence:
    """
    Task 8 title intelligence layer.
    """
    def analyze(self, title: str):
        return analyze_title(title)
    def analyze_channel(
        self,
        channel_id: Optional[str] = None,
        limit: int = 100,
    ):
        return analyze_channel_titles(
            channel_id=channel_id,
            limit=limit,
        )
    def compare(
        self,
        title_a: str,
        title_b: str,
    ):
        return compare_titles(title_a, title_b)
    def variants(
        self,
        base_topic: str,
        count: int = 5,
    ):
        return generate_title_variants(
            base_topic=base_topic,
            count=count,
        )
title_intelligence = YouTubeTitleIntelligence()
