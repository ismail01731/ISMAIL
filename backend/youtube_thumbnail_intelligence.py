import sqlite3
import re
from pathlib import Path
from typing import Optional
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "youtube_growth.db"
def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(DB_PATH))
def _avg(values):
    values = [float(v) for v in values if v is not None]
    return round(sum(values) / len(values), 2) if values else 0.0
def _thumbnail_features(concept: str):
    text = str(concept or "").strip()
    return {
        "concept_length": len(text),
        "word_count": len(re.findall(r"\S+", text)),
        "has_face": any(
            word in text.lower()
            for word in ["face", "reaction", "expression", "মুখ", "রিঅ্যাকশন", "এক্সপ্রেশন"]
        ),
        "has_text": any(
            word in text.lower()
            for word in ["text", "title", "caption", "লেখা", "টেক্সট"]
        ),
        "has_arrow": any(
            symbol in text
            for symbol in ["→", "➜", "➡", "arrow", "তীর"]
        ),
        "has_circle": any(
            word in text.lower()
            for word in ["circle", "highlight", "বৃত্ত", "হাইলাইট"]
        ),
        "has_emotion": any(
            word in text.lower()
            for word in [
                "funny", "shock", "surprise", "happy", "sad",
                "crazy", "মজার", "অবাক", "চমক", "হাসি", "ভয়"
            ]
        ),
        "has_contrast": any(
            word in text.lower()
            for word in [
                "contrast", "bright", "dark", "color", "কনট্রাস্ট",
                "উজ্জ্বল", "ডার্ক", "রঙ"
            ]
        ),
    }
def analyze_thumbnail_concept(concept: str):
    features = _thumbnail_features(concept)
    score = 50
    if 15 <= features["concept_length"] <= 120:
        score += 8
    if 2 <= features["word_count"] <= 15:
        score += 8
    if features["has_face"]:
        score += 8
    if features["has_text"]:
        score += 5
    if features["has_arrow"]:
        score += 4
    if features["has_circle"]:
        score += 4
    if features["has_emotion"]:
        score += 7
    if features["has_contrast"]:
        score += 6
    if features["word_count"] > 20:
        score -= 10
    if features["concept_length"] > 180:
        score -= 12
    score = max(0, min(100, score))
    return {
        "success": True,
        "concept": concept,
        "thumbnail_score": score,
        "features": features,
    }
def analyze_channel_thumbnails(channel_id: Optional[str] = None, limit: int = 100):
    con = _connect()
    con.row_factory = sqlite3.Row
    try:
        if channel_id:
            channel = con.execute(
                """
                SELECT id, channel_id, channel_name
                FROM youtube_channels
                WHERE channel_id = ?
                """,
                (channel_id,),
            ).fetchone()
        else:
            channel = con.execute(
                """
                SELECT id, channel_id, channel_name
                FROM youtube_channels
                ORDER BY id
                LIMIT 1
                """
            ).fetchone()
        if not channel:
            return {
                "success": False,
                "error": "Channel not found",
                "analyzed_video_count": 0,
            }
        rows = con.execute(
            """
            SELECT
                youtube_video_id,
                title,
                views,
                ctr
            FROM youtube_videos
            WHERE channel_id = ?
            ORDER BY views DESC, id DESC
            LIMIT ?
            """,
            (channel["id"], int(limit)),
        ).fetchall()
        results = []
        for row in rows:
            # Existing database does not yet have a dedicated thumbnail
            # concept column, so the title is used as a neutral proxy
            # until thumbnail metadata is collected.
            concept = row["title"] or ""
            analysis = analyze_thumbnail_concept(concept)
            results.append(
                {
                    "youtube_video_id": row["youtube_video_id"],
                    "title": row["title"],
                    "views": int(row["views"] or 0),
                    "ctr": float(row["ctr"]) if row["ctr"] is not None else None,
                    "thumbnail_score": analysis["thumbnail_score"],
                    "features": analysis["features"],
                }
            )
        top_thumbnails = sorted(
            results,
            key=lambda x: (
                x["thumbnail_score"],
                x["views"],
            ),
            reverse=True,
        )[:10]
        return {
            "success": True,
            "channel_id": channel["channel_id"],
            "channel_name": channel["channel_name"],
            "analyzed_video_count": len(results),
            "average_thumbnail_score": _avg(
                [x["thumbnail_score"] for x in results]
            ),
            "average_ctr": _avg(
                [x["ctr"] for x in results if x["ctr"] is not None]
            ),
            "average_views": _avg(
                [x["views"] for x in results]
            ),
            "top_thumbnails": top_thumbnails,
            "thumbnail_patterns": {
                "face_reaction": [
                    x for x in results if x["features"]["has_face"]
                ][:10],
                "text_based": [
                    x for x in results if x["features"]["has_text"]
                ][:10],
                "emotion_based": [
                    x for x in results if x["features"]["has_emotion"]
                ][:10],
                "high_contrast": [
                    x for x in results if x["features"]["has_contrast"]
                ][:10],
            },
        }
    finally:
        con.close()
def compare_thumbnail_concepts(concept_a: str, concept_b: str):
    a = analyze_thumbnail_concept(concept_a)
    b = analyze_thumbnail_concept(concept_b)
    return {
        "success": True,
        "thumbnail_a": a,
        "thumbnail_b": b,
        "score_difference": round(
            a["thumbnail_score"] - b["thumbnail_score"], 2
        ),
    }
def generate_thumbnail_variants(base_topic: str, count: int = 5):
    topic = str(base_topic or "").strip()
    templates = [
        f"{topic} — shocked reaction face + bold text",
        f"{topic} — funny expression + bright contrast",
        f"{topic} — surprised face + arrow highlight",
        f"{topic} — emotional reaction + short text",
        f"{topic} — close-up face + highlighted object",
        f"{topic} — before vs after visual",
        f"{topic} — crazy reaction + circle highlight",
        f"{topic} — village comedy reaction thumbnail",
        f"{topic} — big reaction face + minimal text",
        f"{topic} — mystery expression + highlighted subject",
    ]
    variants = []
    for template in templates[:10]:
        analysis = analyze_thumbnail_concept(template)
        variants.append(
            {
                "concept": template,
                "thumbnail_score": analysis["thumbnail_score"],
                "features": analysis["features"],
            }
        )
    variants.sort(
        key=lambda x: x["thumbnail_score"],
        reverse=True,
    )
    count = max(1, min(int(count), 10))
    return {
        "success": True,
        "base_topic": topic,
        "variants": variants[:count],
    }
class YouTubeThumbnailIntelligence:
    def analyze(self, concept: str):
        return analyze_thumbnail_concept(concept)
    def analyze_channel(self, channel_id: Optional[str] = None, limit: int = 100):
        return analyze_channel_thumbnails(channel_id, limit)
    def compare(self, concept_a: str, concept_b: str):
        return compare_thumbnail_concepts(concept_a, concept_b)
    def variants(self, base_topic: str, count: int = 5):
        return generate_thumbnail_variants(base_topic, count)
thumbnail_intelligence = YouTubeThumbnailIntelligence()
