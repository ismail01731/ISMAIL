import sqlite3
from pathlib import Path
from typing import Optional
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "youtube_growth.db"
def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(DB_PATH))
def _row_to_dict(row):
    return dict(row) if row is not None else None
def capture_snapshot(
    video_id: int,
    views: int = 0,
    likes: int = 0,
    comments: int = 0,
    shares: int = 0,
    subscribers_gained: int = 0,
    impressions: int = 0,
    ctr: Optional[float] = None,
    average_view_duration_seconds: Optional[float] = None,
    average_percentage_viewed: Optional[float] = None,
    traffic_source: Optional[str] = None,
):
    con = _connect()
    try:
        cur = con.execute(
            """
            INSERT INTO youtube_video_snapshots
            (
                video_id,
                views,
                likes,
                comments,
                shares,
                subscribers_gained,
                impressions,
                ctr,
                average_view_duration_seconds,
                average_percentage_viewed,
                traffic_source
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                int(video_id),
                int(views),
                int(likes),
                int(comments),
                int(shares),
                int(subscribers_gained),
                int(impressions),
                float(ctr) if ctr is not None else None,
                float(average_view_duration_seconds)
                if average_view_duration_seconds is not None
                else None,
                float(average_percentage_viewed)
                if average_percentage_viewed is not None
                else None,
                traffic_source,
            ),
        )
        con.commit()
        return {
            "success": True,
            "snapshot_id": cur.lastrowid,
            "video_id": int(video_id),
        }
    finally:
        con.close()
def get_video_snapshots(
    video_id: int,
    limit: int = 100,
):
    con = _connect()
    con.row_factory = sqlite3.Row
    try:
        rows = con.execute(
            """
            SELECT *
            FROM youtube_video_snapshots
            WHERE video_id = ?
            ORDER BY captured_at ASC, id ASC
            LIMIT ?
            """,
            (int(video_id), int(limit)),
        ).fetchall()
        return {
            "success": True,
            "video_id": int(video_id),
            "count": len(rows),
            "snapshots": [
                _row_to_dict(row)
                for row in rows
            ],
        }
    finally:
        con.close()
def calculate_growth(
    first_snapshot: dict,
    last_snapshot: dict,
):
    def delta(field):
        return (
            float(last_snapshot.get(field) or 0)
            - float(first_snapshot.get(field) or 0)
        )
    first_views = float(first_snapshot.get("views") or 0)
    last_views = float(last_snapshot.get("views") or 0)
    if first_views > 0:
        views_growth_percent = round(
            ((last_views - first_views) / first_views) * 100,
            2,
        )
    else:
        views_growth_percent = 0.0
    return {
        "views_change": delta("views"),
        "likes_change": delta("likes"),
        "comments_change": delta("comments"),
        "shares_change": delta("shares"),
        "subscribers_gained_change": delta(
            "subscribers_gained"
        ),
        "impressions_change": delta("impressions"),
        "views_growth_percent": views_growth_percent,
        "ctr_change": round(
            float(last_snapshot.get("ctr") or 0)
            - float(first_snapshot.get("ctr") or 0),
            2,
        ),
        "retention_change": round(
            float(
                last_snapshot.get(
                    "average_percentage_viewed"
                )
                or 0
            )
            - float(
                first_snapshot.get(
                    "average_percentage_viewed"
                )
                or 0
            ),
            2,
        ),
    }
def analyze_post_publish(
    video_id: int,
):
    con = _connect()
    con.row_factory = sqlite3.Row
    try:
        video = con.execute(
            """
            SELECT
                id,
                youtube_video_id,
                title,
                views,
                likes,
                comments,
                subscribers_gained,
                impressions,
                ctr,
                average_view_duration_seconds,
                average_percentage_viewed,
                published_at
            FROM youtube_videos
            WHERE id = ?
            """,
            (int(video_id),),
        ).fetchone()
        if not video:
            return {
                "success": False,
                "error": "Video not found",
            }
        snapshots = con.execute(
            """
            SELECT *
            FROM youtube_video_snapshots
            WHERE video_id = ?
            ORDER BY captured_at ASC, id ASC
            """,
            (int(video_id),),
        ).fetchall()
        snapshot_dicts = [
            _row_to_dict(row)
            for row in snapshots
        ]
        if not snapshot_dicts:
            return {
                "success": True,
                "video_id": int(video_id),
                "youtube_video_id": video["youtube_video_id"],
                "title": video["title"],
                "snapshot_count": 0,
                "growth": {},
                "trend": "no_snapshot_data",
                "latest_snapshot": None,
            }
        first = snapshot_dicts[0]
        latest = snapshot_dicts[-1]
        growth = calculate_growth(
            first,
            latest,
        )
        if len(snapshot_dicts) >= 2:
            previous = snapshot_dicts[-2]
            latest_view_change = (
                float(latest.get("views") or 0)
                - float(previous.get("views") or 0)
            )
            if latest_view_change > 0:
                trend = "growing"
            elif latest_view_change < 0:
                trend = "declining"
            else:
                trend = "flat"
        else:
            trend = "initial"
        latest_ctr = latest.get("ctr")
        latest_retention = latest.get(
            "average_percentage_viewed"
        )
        performance_signals = []
        if latest_ctr is not None:
            if float(latest_ctr) >= 8:
                performance_signals.append(
                    "strong_ctr"
                )
            elif float(latest_ctr) < 3:
                performance_signals.append(
                    "low_ctr"
                )
        if latest_retention is not None:
            if float(latest_retention) >= 70:
                performance_signals.append(
                    "strong_retention"
                )
            elif float(latest_retention) < 40:
                performance_signals.append(
                    "low_retention"
                )
        if growth["views_growth_percent"] > 50:
            performance_signals.append(
                "strong_view_growth"
            )
        return {
            "success": True,
            "video_id": int(video_id),
            "youtube_video_id": video["youtube_video_id"],
            "title": video["title"],
            "published_at": video["published_at"],
            "snapshot_count": len(snapshot_dicts),
            "first_snapshot": first,
            "latest_snapshot": latest,
            "growth": growth,
            "trend": trend,
            "performance_signals": performance_signals,
        }
    finally:
        con.close()
def analyze_channel_post_publish(
    channel_id: Optional[str] = None,
    limit: int = 100,
):
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
            }
        videos = con.execute(
            """
            SELECT
                id,
                youtube_video_id,
                title,
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
            (
                channel["id"],
                int(limit),
            ),
        ).fetchall()
        results = []
        for video in videos:
            snapshots = con.execute(
                """
                SELECT *
                FROM youtube_video_snapshots
                WHERE video_id = ?
                ORDER BY captured_at ASC, id ASC
                """,
                (video["id"],),
            ).fetchall()
            snapshot_count = len(snapshots)
            if snapshot_count >= 2:
                first = _row_to_dict(snapshots[0])
                latest = _row_to_dict(snapshots[-1])
                growth = calculate_growth(
                    first,
                    latest,
                )
            else:
                growth = {}
            results.append(
                {
                    "video_id": video["id"],
                    "youtube_video_id": video[
                        "youtube_video_id"
                    ],
                    "title": video["title"],
                    "views": int(video["views"] or 0),
                    "ctr": (
                        float(video["ctr"])
                        if video["ctr"] is not None
                        else None
                    ),
                    "retention": (
                        float(
                            video[
                                "average_percentage_viewed"
                            ]
                        )
                        if video[
                            "average_percentage_viewed"
                        ] is not None
                        else None
                    ),
                    "snapshot_count": snapshot_count,
                    "growth": growth,
                }
            )
        return {
            "success": True,
            "channel_id": channel["channel_id"],
            "channel_name": channel["channel_name"],
            "analyzed_video_count": len(results),
            "videos": results,
        }
    finally:
        con.close()
class YouTubePostPublishAnalytics:
    def capture_snapshot(
        self,
        video_id: int,
        views: int = 0,
        likes: int = 0,
        comments: int = 0,
        shares: int = 0,
        subscribers_gained: int = 0,
        impressions: int = 0,
        ctr: Optional[float] = None,
        average_view_duration_seconds: Optional[float] = None,
        average_percentage_viewed: Optional[float] = None,
        traffic_source: Optional[str] = None,
    ):
        return capture_snapshot(
            video_id,
            views,
            likes,
            comments,
            shares,
            subscribers_gained,
            impressions,
            ctr,
            average_view_duration_seconds,
            average_percentage_viewed,
            traffic_source,
        )
    def snapshots(
        self,
        video_id: int,
        limit: int = 100,
    ):
        return get_video_snapshots(
            video_id,
            limit,
        )
    def analyze_video(self, video_id: int):
        return analyze_post_publish(video_id)
    def analyze_channel(
        self,
        channel_id: Optional[str] = None,
        limit: int = 100,
    ):
        return analyze_channel_post_publish(
            channel_id,
            limit,
        )
post_publish_analytics = YouTubePostPublishAnalytics()
