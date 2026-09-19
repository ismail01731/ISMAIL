import sqlite3
from pathlib import Path
from typing import Optional
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "youtube_growth.db"
def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
def _avg(values):
    values = [float(v) for v in values if v is not None]
    return round(sum(values) / len(values), 2) if values else 0.0
def save_channel(
    channel_id: Optional[str],
    channel_name: str,
    handle: Optional[str] = None,
    niche: Optional[str] = None,
    language: Optional[str] = None,
    country: Optional[str] = None,
    subscriber_count: int = 0,
    video_count: int = 0,
    view_count: int = 0,
):
    channel_name = str(channel_name or "").strip()
    if not channel_name:
        raise ValueError("channel_name is required")
    with _connect() as conn:
        existing = None
        if channel_id:
            existing = conn.execute(
                "SELECT id FROM youtube_channels WHERE channel_id = ?",
                (channel_id,),
            ).fetchone()
        if existing:
            conn.execute(
                """
                UPDATE youtube_channels
                SET channel_name = ?,
                    handle = ?,
                    niche = ?,
                    language = ?,
                    country = ?,
                    subscriber_count = ?,
                    video_count = ?,
                    view_count = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    channel_name,
                    handle,
                    niche,
                    language,
                    country,
                    int(subscriber_count or 0),
                    int(video_count or 0),
                    int(view_count or 0),
                    existing["id"],
                ),
            )
            channel_db_id = existing["id"]
        else:
            cursor = conn.execute(
                """
                INSERT INTO youtube_channels (
                    channel_id,
                    channel_name,
                    handle,
                    niche,
                    language,
                    country,
                    subscriber_count,
                    video_count,
                    view_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    channel_id,
                    channel_name,
                    handle,
                    niche,
                    language,
                    country,
                    int(subscriber_count or 0),
                    int(video_count or 0),
                    int(view_count or 0),
                ),
            )
            channel_db_id = cursor.lastrowid
        conn.commit()
        row = conn.execute(
            "SELECT * FROM youtube_channels WHERE id = ?",
            (channel_db_id,),
        ).fetchone()
        return dict(row)
def get_channel(channel_id: Optional[str] = None):
    with _connect() as conn:
        if channel_id:
            row = conn.execute(
                "SELECT * FROM youtube_channels WHERE channel_id = ?",
                (channel_id,),
            ).fetchone()
        else:
            row = conn.execute(
                "SELECT * FROM youtube_channels ORDER BY id DESC LIMIT 1"
            ).fetchone()
        return dict(row) if row else None
def list_channels():
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM youtube_channels
            ORDER BY updated_at DESC, id DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]
def save_video(
    youtube_video_id: str,
    title: str,
    channel_id: Optional[str] = None,
    description: Optional[str] = None,
    topic: Optional[str] = None,
    format: Optional[str] = None,
    duration_seconds: float = 0,
    published_at: Optional[str] = None,
    views: int = 0,
    likes: int = 0,
    comments: int = 0,
    shares: int = 0,
    subscribers_gained: int = 0,
    impressions: int = 0,
    ctr: Optional[float] = None,
    average_view_duration_seconds: Optional[float] = None,
    average_percentage_viewed: Optional[float] = None,
):
    youtube_video_id = str(youtube_video_id or "").strip()
    title = str(title or "").strip()
    if not youtube_video_id:
        raise ValueError("youtube_video_id is required")
    if not title:
        raise ValueError("title is required")
    with _connect() as conn:
        channel_db_id = None
        if channel_id:
            channel = conn.execute(
                """
                SELECT id
                FROM youtube_channels
                WHERE channel_id = ?
                """,
                (channel_id,),
            ).fetchone()
            if not channel:
                raise ValueError("YouTube channel not found")
            channel_db_id = channel["id"]
        existing = conn.execute(
            """
            SELECT id
            FROM youtube_videos
            WHERE youtube_video_id = ?
            """,
            (youtube_video_id,),
        ).fetchone()
        values = (
            title,
            description,
            topic,
            format,
            float(duration_seconds or 0),
            published_at,
            int(views or 0),
            int(likes or 0),
            int(comments or 0),
            int(shares or 0),
            int(subscribers_gained or 0),
            int(impressions or 0),
            ctr,
            average_view_duration_seconds,
            average_percentage_viewed,
        )
        if existing:
            if channel_db_id is not None:
                conn.execute(
                    """
                    UPDATE youtube_videos
                    SET channel_id = ?,
                        title = ?,
                        description = ?,
                        topic = ?,
                        format = ?,
                        duration_seconds = ?,
                        published_at = ?,
                        views = ?,
                        likes = ?,
                        comments = ?,
                        shares = ?,
                        subscribers_gained = ?,
                        impressions = ?,
                        ctr = ?,
                        average_view_duration_seconds = ?,
                        average_percentage_viewed = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (channel_db_id, *values, existing["id"]),
                )
            else:
                conn.execute(
                    """
                    UPDATE youtube_videos
                    SET title = ?,
                        description = ?,
                        topic = ?,
                        format = ?,
                        duration_seconds = ?,
                        published_at = ?,
                        views = ?,
                        likes = ?,
                        comments = ?,
                        shares = ?,
                        subscribers_gained = ?,
                        impressions = ?,
                        ctr = ?,
                        average_view_duration_seconds = ?,
                        average_percentage_viewed = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (*values, existing["id"]),
                )
            video_db_id = existing["id"]
        else:
            if channel_db_id is None:
                raise ValueError("channel_id is required for a new video")
            cursor = conn.execute(
                """
                INSERT INTO youtube_videos (
                    channel_id,
                    youtube_video_id,
                    title,
                    description,
                    topic,
                    format,
                    duration_seconds,
                    published_at,
                    views,
                    likes,
                    comments,
                    shares,
                    subscribers_gained,
                    impressions,
                    ctr,
                    average_view_duration_seconds,
                    average_percentage_viewed
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    channel_db_id,
                    youtube_video_id,
                    *values,
                ),
            )
            video_db_id = cursor.lastrowid
        conn.commit()
        row = conn.execute(
            """
            SELECT
                v.*,
                c.channel_id AS youtube_channel_id,
                c.channel_name
            FROM youtube_videos v
            JOIN youtube_channels c
                ON c.id = v.channel_id
            WHERE v.id = ?
            """,
            (video_db_id,),
        ).fetchone()
        return dict(row)
def get_video(youtube_video_id: str):
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT
                v.*,
                c.channel_id AS youtube_channel_id,
                c.channel_name
            FROM youtube_videos v
            JOIN youtube_channels c
                ON c.id = v.channel_id
            WHERE v.youtube_video_id = ?
            """,
            (youtube_video_id,),
        ).fetchone()
        return dict(row) if row else None
def list_videos(channel_id: Optional[str] = None, limit: int = 100):
    limit = max(1, min(int(limit or 100), 1000))
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
                ORDER BY
                    COALESCE(v.published_at, v.created_at) DESC,
                    v.id DESC
                LIMIT ?
                """,
                (channel_id, limit),
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
                ORDER BY
                    COALESCE(v.published_at, v.created_at) DESC,
                    v.id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]
def save_topic(
    topic: str,
    category: Optional[str] = None,
    source: Optional[str] = None,
    trend_score: float = 0.0,
    opportunity_score: float = 0.0,
    competition_score: float = 0.0,
):
    topic = str(topic or "").strip()
    if not topic:
        raise ValueError("topic is required")
    with _connect() as conn:
        existing = conn.execute(
            """
            SELECT id
            FROM youtube_topics
            WHERE topic = ?
              AND COALESCE(category, '') = COALESCE(?, '')
            ORDER BY id DESC
            LIMIT 1
            """,
            (topic, category),
        ).fetchone()
        if existing:
            conn.execute(
                """
                UPDATE youtube_topics
                SET source = ?,
                    trend_score = ?,
                    opportunity_score = ?,
                    competition_score = ?,
                    collected_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    source,
                    float(trend_score or 0),
                    float(opportunity_score or 0),
                    float(competition_score or 0),
                    existing["id"],
                ),
            )
            topic_id = existing["id"]
        else:
            cursor = conn.execute(
                """
                INSERT INTO youtube_topics (
                    topic,
                    category,
                    source,
                    trend_score,
                    opportunity_score,
                    competition_score
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    topic,
                    category,
                    source,
                    float(trend_score or 0),
                    float(opportunity_score or 0),
                    float(competition_score or 0),
                ),
            )
            topic_id = cursor.lastrowid
        conn.commit()
        row = conn.execute(
            "SELECT * FROM youtube_topics WHERE id = ?",
            (topic_id,),
        ).fetchone()
        return dict(row)
def get_topic(topic_id: int):
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM youtube_topics WHERE id = ?",
            (int(topic_id),),
        ).fetchone()
        return dict(row) if row else None
def list_topics(
    category: Optional[str] = None,
    source: Optional[str] = None,
    limit: int = 100,
):
    limit = max(1, min(int(limit or 100), 1000))
    with _connect() as conn:
        conditions = []
        params = []
        if category:
            conditions.append("category = ?")
            params.append(category)
        if source:
            conditions.append("source = ?")
            params.append(source)
        where = ""
        if conditions:
            where = "WHERE " + " AND ".join(conditions)
        rows = conn.execute(
            f"""
            SELECT *
            FROM youtube_topics
            {where}
            ORDER BY
                opportunity_score DESC,
                trend_score DESC,
                collected_at DESC,
                id DESC
            LIMIT ?
            """,
            (*params, limit),
        ).fetchall()
        return [dict(row) for row in rows]
def get_top_topics(limit: int = 10):
    topics = list_topics(limit=limit)
    return {
        "success": True,
        "count": len(topics),
        "topics": topics,
    }
def analyze_topic_opportunities(limit: int = 20):
    topics = list_topics(limit=limit)
    return {
        "success": True,
        "count": len(topics),
        "topics": topics,
    }
def save_competitor(
    channel_id: str,
    channel_name: str,
    handle: Optional[str] = None,
    niche: Optional[str] = None,
    language: Optional[str] = None,
    country: Optional[str] = None,
    subscriber_count: int = 0,
    video_count: int = 0,
    view_count: int = 0,
    notes: Optional[str] = None,
):
    channel_id = str(channel_id or "").strip()
    channel_name = str(channel_name or "").strip()
    if not channel_id:
        raise ValueError("competitor channel_id is required")
    if not channel_name:
        raise ValueError("competitor channel_name is required")
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS youtube_competitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT NOT NULL UNIQUE,
                channel_name TEXT NOT NULL,
                handle TEXT,
                niche TEXT,
                language TEXT,
                country TEXT,
                subscriber_count INTEGER DEFAULT 0,
                video_count INTEGER DEFAULT 0,
                view_count INTEGER DEFAULT 0,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        existing = conn.execute(
            """
            SELECT id
            FROM youtube_competitors
            WHERE channel_id = ?
            """,
            (channel_id,),
        ).fetchone()
        if existing:
            conn.execute(
                """
                UPDATE youtube_competitors
                SET channel_name = ?,
                    handle = ?,
                    niche = ?,
                    language = ?,
                    country = ?,
                    subscriber_count = ?,
                    video_count = ?,
                    view_count = ?,
                    notes = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    channel_name,
                    handle,
                    niche,
                    language,
                    country,
                    int(subscriber_count or 0),
                    int(video_count or 0),
                    int(view_count or 0),
                    notes,
                    existing["id"],
                ),
            )
            competitor_id = existing["id"]
        else:
            cursor = conn.execute(
                """
                INSERT INTO youtube_competitors (
                    channel_id,
                    channel_name,
                    handle,
                    niche,
                    language,
                    country,
                    subscriber_count,
                    video_count,
                    view_count,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    channel_id,
                    channel_name,
                    handle,
                    niche,
                    language,
                    country,
                    int(subscriber_count or 0),
                    int(video_count or 0),
                    int(view_count or 0),
                    notes,
                ),
            )
            competitor_id = cursor.lastrowid
        conn.commit()
        row = conn.execute(
            """
            SELECT *
            FROM youtube_competitors
            WHERE id = ?
            """,
            (competitor_id,),
        ).fetchone()
        return dict(row)
def get_competitor(channel_id: str):
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM youtube_competitors
            WHERE channel_id = ?
            """,
            (channel_id,),
        ).fetchone()
        return dict(row) if row else None
def list_competitors(limit: int = 100):
    limit = max(1, min(int(limit or 100), 1000))
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM youtube_competitors
            ORDER BY updated_at DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]
def analyze_competitors(limit: int = 100):
    competitors = list_competitors(limit)
    if not competitors:
        return {
            "success": True,
            "competitor_count": 0,
            "total_subscribers": 0,
            "average_subscribers": 0.0,
            "average_views": 0.0,
            "top_competitors": [],
        }
    ranked = sorted(
        competitors,
        key=lambda x: (
            int(x.get("view_count") or 0),
            int(x.get("subscriber_count") or 0),
        ),
        reverse=True,
    )
    return {
        "success": True,
        "competitor_count": len(competitors),
        "total_subscribers": sum(
            int(x.get("subscriber_count") or 0)
            for x in competitors
        ),
        "average_subscribers": _avg(
            [x.get("subscriber_count") for x in competitors]
        ),
        "average_views": _avg(
            [x.get("view_count") for x in competitors]
        ),
        "top_competitors": ranked[:10],
    }
def detect_content_opportunities(
    channel_id: Optional[str] = None,
    limit: int = 20,
):
    limit = max(1, min(int(limit or 20), 100))
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
                SELECT *
                FROM youtube_videos
                WHERE channel_id = ?
                ORDER BY views DESC, id DESC
                """,
                (channel["id"],),
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
            videos = []
            if channel:
                videos = conn.execute(
                    """
                    SELECT *
                    FROM youtube_videos
                    WHERE channel_id = ?
                    ORDER BY views DESC, id DESC
                    """,
                    (channel["id"],),
                ).fetchall()
        topics = conn.execute(
            """
            SELECT *
            FROM youtube_topics
            ORDER BY opportunity_score DESC,
                     trend_score DESC,
                     id DESC
            LIMIT 1000
            """
        ).fetchall()
        competitor_table = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'youtube_competitors'
            """
        ).fetchone()
        competitors = []
        if competitor_table:
            competitors = conn.execute(
                "SELECT * FROM youtube_competitors"
            ).fetchall()
    videos = [dict(v) for v in videos]
    topics = [dict(t) for t in topics]
    competitors = [dict(c) for c in competitors]
    topic_performance = {}
    for video in videos:
        topic = (video.get("topic") or "").strip().lower()
        if not topic:
            continue
        topic_performance.setdefault(topic, []).append(video)
    opportunities = []
    for topic in topics:
        name = str(topic.get("topic") or "").strip()
        if not name:
            continue
        key = name.lower()
        trend = float(topic.get("trend_score") or 0)
        stored_opportunity = float(topic.get("opportunity_score") or 0)
        competition = float(topic.get("competition_score") or 0)
        historical = topic_performance.get(key, [])
        historical_views = _avg(
            [v.get("views") for v in historical]
        )
        historical_retention = _avg(
            [v.get("average_percentage_viewed") for v in historical]
        )
        signal = (
            trend * 0.35
            + stored_opportunity * 0.40
            + max(0.0, 100.0 - competition) * 0.15
        )
        if historical:
            signal += min(historical_views / 1000.0, 100.0) * 0.05
            signal += historical_retention * 0.05
        signal = round(min(max(signal, 0.0), 100.0), 2)
        opportunities.append(
            {
                "topic": name,
                "category": topic.get("category"),
                "source": topic.get("source"),
                "trend_score": trend,
                "opportunity_score": stored_opportunity,
                "competition_score": competition,
                "historical_video_count": len(historical),
                "historical_average_views": historical_views,
                "historical_average_retention": historical_retention,
                "opportunity_signal": signal,
                "has_channel_evidence": bool(historical),
                "competitor_count": len(competitors),
            }
        )
    opportunities.sort(
        key=lambda x: x["opportunity_signal"],
        reverse=True,
    )
    return {
        "success": True,
        "channel_id": channel["channel_id"] if channel else None,
        "channel_name": channel["channel_name"] if channel else None,
        "topic_count": len(topics),
        "competitor_count": len(competitors),
        "historical_video_count": len(videos),
        "opportunities": opportunities[:limit],
    }
def youtube_growth_db_status():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS youtube_competitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT NOT NULL UNIQUE,
                channel_name TEXT NOT NULL,
                handle TEXT,
                niche TEXT,
                language TEXT,
                country TEXT,
                subscriber_count INTEGER DEFAULT 0,
                video_count INTEGER DEFAULT 0,
                view_count INTEGER DEFAULT 0,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        tables = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        ).fetchall()
        return {
            "database": str(DB_PATH),
            "tables": [row["name"] for row in tables],
        }
def analyze_hook_retention(
    channel_id: Optional[str] = None,
    limit: int = 20,
):
    """
    Analyze hook/retention-related signals from stored YouTube video
    analytics.
    The current database stores average percentage viewed and average
    view duration. These metrics are used as retention evidence.
    Hook strength is represented as a signal, not a guarantee of future
    performance.
    """
    limit = max(1, min(int(limit or 20), 100))
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
            rows = conn.execute(
                """
                SELECT *
                FROM youtube_videos
                WHERE channel_id = ?
                  AND (
                      average_percentage_viewed IS NOT NULL
                      OR average_view_duration_seconds IS NOT NULL
                  )
                ORDER BY views DESC, id DESC
                """,
                (channel["id"],),
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
                rows = conn.execute(
                    """
                    SELECT *
                    FROM youtube_videos
                    WHERE channel_id = ?
                      AND (
                          average_percentage_viewed IS NOT NULL
                          OR average_view_duration_seconds IS NOT NULL
                      )
                    ORDER BY views DESC, id DESC
                    """,
                    (channel["id"],),
                ).fetchall()
            else:
                rows = []
    videos = [dict(row) for row in rows]
    if not videos:
        return {
            "success": True,
            "channel_id": channel["channel_id"] if channel else None,
            "channel_name": channel["channel_name"] if channel else None,
            "analyzed_video_count": 0,
            "average_retention": 0.0,
            "average_view_duration": 0.0,
            "retention_signal": 0.0,
            "top_retention_videos": [],
            "hook_insights": [],
        }
    retention_values = [
        v.get("average_percentage_viewed")
        for v in videos
        if v.get("average_percentage_viewed") is not None
    ]
    duration_values = [
        v.get("average_view_duration_seconds")
        for v in videos
        if v.get("average_view_duration_seconds") is not None
    ]
    average_retention = _avg(retention_values)
    average_duration = _avg(duration_values)
    ranked = sorted(
        videos,
        key=lambda v: (
            float(v.get("average_percentage_viewed") or 0),
            int(v.get("views") or 0),
        ),
        reverse=True,
    )
    top_videos = []
    for video in ranked[:limit]:
        retention = float(
            video.get("average_percentage_viewed") or 0
        )
        duration = float(
            video.get("average_view_duration_seconds") or 0
        )
        if retention >= 70:
            strength = "strong"
        elif retention >= 50:
            strength = "moderate"
        else:
            strength = "needs_improvement"
        top_videos.append(
            {
                "youtube_video_id": video.get("youtube_video_id"),
                "title": video.get("title"),
                "views": int(video.get("views") or 0),
                "average_percentage_viewed": retention,
                "average_view_duration_seconds": duration,
                "retention_strength": strength,
            }
        )
    retention_signal = round(
        min(max(average_retention, 0.0), 100.0),
        2,
    )
    hook_insights = []
    if average_retention >= 70:
        hook_insights.append(
            "Stored videos show strong retention; preserve the opening structure for further testing."
        )
    elif average_retention >= 50:
        hook_insights.append(
            "Stored videos show moderate retention; test stronger opening hooks and faster early pacing."
        )
    else:
        hook_insights.append(
            "Stored videos show lower retention; test shorter introductions and earlier delivery of the main payoff."
        )
    return {
        "success": True,
        "channel_id": channel["channel_id"] if channel else None,
        "channel_name": channel["channel_name"] if channel else None,
        "analyzed_video_count": len(videos),
        "average_retention": average_retention,
        "average_view_duration": average_duration,
        "retention_signal": retention_signal,
        "top_retention_videos": top_videos,
        "hook_insights": hook_insights,
    }
