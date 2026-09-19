import sqlite3
from pathlib import Path
from typing import Optional
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "youtube_growth.db"
def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn
def _avg(values):
    values = [float(v) for v in values if v is not None]
    return round(sum(values) / len(values), 2) if values else 0.0
def analyze_channel(channel_id: Optional[str] = None):
    with _connect() as conn:
        if channel_id:
            rows = conn.execute(
                """
                SELECT
                    v.*,
                    c.channel_id AS youtube_channel_id,
                    c.channel_name
                FROM youtube_videos v
                JOIN youtube_channels c
                    ON c.id = v.channel_id
                WHERE c.channel_id = ?
                ORDER BY v.views DESC, v.id DESC
                """,
                (channel_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT
                    v.*,
                    c.channel_id AS youtube_channel_id,
                    c.channel_name
                FROM youtube_videos v
                JOIN youtube_channels c
                    ON c.id = v.channel_id
                ORDER BY v.views DESC, v.id DESC
                """
            ).fetchall()
    videos = [dict(row) for row in rows]
    if not videos:
        return {
            "success": True,
            "video_count": 0,
            "total_views": 0,
            "average_views": 0.0,
            "average_likes": 0.0,
            "average_comments": 0.0,
            "average_ctr": 0.0,
            "average_retention": 0.0,
            "top_videos": [],
            "topic_patterns": [],
            "format_patterns": [],
        }
    topic_groups = {}
    format_groups = {}
    for video in videos:
        topic = (video.get("topic") or "Unknown").strip() or "Unknown"
        fmt = (video.get("format") or "Unknown").strip() or "Unknown"
        topic_groups.setdefault(topic, []).append(video)
        format_groups.setdefault(fmt, []).append(video)
    def group_summary(name, items):
        return {
            "name": name,
            "video_count": len(items),
            "total_views": sum(int(v.get("views") or 0) for v in items),
            "average_views": _avg([v.get("views") for v in items]),
            "average_likes": _avg([v.get("likes") for v in items]),
            "average_comments": _avg([v.get("comments") for v in items]),
            "average_ctr": _avg([v.get("ctr") for v in items]),
            "average_retention": _avg(
                [v.get("average_percentage_viewed") for v in items]
            ),
        }
    topic_patterns = [
        group_summary(name, items)
        for name, items in topic_groups.items()
    ]
    format_patterns = [
        group_summary(name, items)
        for name, items in format_groups.items()
    ]
    topic_patterns.sort(key=lambda x: x["average_views"], reverse=True)
    format_patterns.sort(key=lambda x: x["average_views"], reverse=True)
    top_videos = [
        {
            "youtube_video_id": v["youtube_video_id"],
            "title": v["title"],
            "topic": v.get("topic"),
            "format": v.get("format"),
            "views": int(v.get("views") or 0),
            "likes": int(v.get("likes") or 0),
            "comments": int(v.get("comments") or 0),
            "ctr": v.get("ctr"),
            "retention": v.get("average_percentage_viewed"),
        }
        for v in videos[:10]
    ]
    return {
        "success": True,
        "video_count": len(videos),
        "total_views": sum(int(v.get("views") or 0) for v in videos),
        "average_views": _avg([v.get("views") for v in videos]),
        "average_likes": _avg([v.get("likes") for v in videos]),
        "average_comments": _avg([v.get("comments") for v in videos]),
        "average_ctr": _avg([v.get("ctr") for v in videos]),
        "average_retention": _avg(
            [v.get("average_percentage_viewed") for v in videos]
        ),
        "top_videos": top_videos,
        "topic_patterns": topic_patterns,
        "format_patterns": format_patterns,
    }
def get_top_patterns(channel_id: Optional[str] = None):
    result = analyze_channel(channel_id)
    return {
        "success": result["success"],
        "video_count": result["video_count"],
        "top_topic": (
            result["topic_patterns"][0]
            if result["topic_patterns"]
            else None
        ),
        "top_format": (
            result["format_patterns"][0]
            if result["format_patterns"]
            else None
        ),
        "top_videos": result["top_videos"],
    }
