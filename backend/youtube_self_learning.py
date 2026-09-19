import json
import sqlite3
from pathlib import Path
from typing import Optional
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "youtube_growth.db"
def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn
def _ensure_learning_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS youtube_learning (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature TEXT NOT NULL,
            pattern TEXT NOT NULL,
            evidence_count INTEGER DEFAULT 0,
            average_performance REAL,
            confidence REAL DEFAULT 0.0,
            metadata TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
def _confidence(evidence_count: int, performance: float):
    evidence_score = min(int(evidence_count), 10) / 10.0
    performance_score = min(max(float(performance), 0.0), 100.0) / 100.0
    return round(
        (evidence_score * 0.6) +
        (performance_score * 0.4),
        3,
    )
def save_learning(
    feature: str,
    pattern: str,
    evidence_count: int = 1,
    average_performance: Optional[float] = None,
    confidence: Optional[float] = None,
    metadata: Optional[dict] = None,
):
    feature = str(feature or "").strip()
    pattern = str(pattern or "").strip()
    if not feature:
        raise ValueError("feature is required")
    if not pattern:
        raise ValueError("pattern is required")
    with _connect() as conn:
        _ensure_learning_table(conn)
        if confidence is None:
            confidence = _confidence(
                evidence_count,
                average_performance or 0.0,
            )
        metadata_json = (
            json.dumps(metadata, ensure_ascii=False)
            if metadata is not None
            else None
        )
        existing = conn.execute(
            """
            SELECT id
            FROM youtube_learning
            WHERE feature = ? AND pattern = ?
            ORDER BY id
            LIMIT 1
            """,
            (feature, pattern),
        ).fetchone()
        if existing:
            conn.execute(
                """
                UPDATE youtube_learning
                SET evidence_count = ?,
                    average_performance = ?,
                    confidence = ?,
                    metadata = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    int(evidence_count),
                    (
                        float(average_performance)
                        if average_performance is not None
                        else None
                    ),
                    float(confidence),
                    metadata_json,
                    existing["id"],
                ),
            )
            learning_id = existing["id"]
        else:
            cur = conn.execute(
                """
                INSERT INTO youtube_learning (
                    feature,
                    pattern,
                    evidence_count,
                    average_performance,
                    confidence,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    feature,
                    pattern,
                    int(evidence_count),
                    (
                        float(average_performance)
                        if average_performance is not None
                        else None
                    ),
                    float(confidence),
                    metadata_json,
                ),
            )
            learning_id = cur.lastrowid
        conn.commit()
        return {
            "success": True,
            "learning_id": learning_id,
            "feature": feature,
            "pattern": pattern,
            "evidence_count": int(evidence_count),
            "average_performance": average_performance,
            "confidence": float(confidence),
        }
def get_learnings(
    feature: Optional[str] = None,
    limit: int = 100,
):
    with _connect() as conn:
        _ensure_learning_table(conn)
        if feature:
            rows = conn.execute(
                """
                SELECT *
                FROM youtube_learning
                WHERE feature = ?
                ORDER BY confidence DESC, evidence_count DESC, id DESC
                LIMIT ?
                """,
                (feature, int(limit)),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT *
                FROM youtube_learning
                ORDER BY confidence DESC, evidence_count DESC, id DESC
                LIMIT ?
                """,
                (int(limit),),
            ).fetchall()
        result = []
        for row in rows:
            item = dict(row)
            if item.get("metadata"):
                try:
                    item["metadata"] = json.loads(
                        item["metadata"]
                    )
                except Exception:
                    pass
            result.append(item)
        return {
            "success": True,
            "count": len(result),
            "learnings": result,
        }
def learn_from_videos(
    channel_db_id: int,
):
    with _connect() as conn:
        _ensure_learning_table(conn)
        videos = conn.execute(
            """
            SELECT
                id,
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
            ORDER BY id ASC
            """,
            (int(channel_db_id),),
        ).fetchall()
        if not videos:
            return {
                "success": True,
                "video_count": 0,
                "new_learnings": [],
            }
        groups = {}
        for video in videos:
            if video["topic"]:
                key = (
                    "topic",
                    str(video["topic"]).strip(),
                )
                groups.setdefault(
                    key,
                    [],
                ).append(video)
            if video["format"]:
                key = (
                    "format",
                    str(video["format"]).strip(),
                )
                groups.setdefault(
                    key,
                    [],
                ).append(video)
        new_learnings = []
        for (feature, pattern), rows in groups.items():
            views = [
                float(row["views"] or 0)
                for row in rows
            ]
            retentions = [
                float(row["average_percentage_viewed"])
                for row in rows
                if row["average_percentage_viewed"]
                is not None
            ]
            average_views = (
                sum(views) / len(views)
                if views
                else 0.0
            )
            average_retention = (
                sum(retentions) / len(retentions)
                if retentions
                else 0.0
            )
            performance = min(
                100.0,
                (
                    min(average_views / 1000.0, 100.0)
                    + average_retention
                ) / 2.0,
            )
            saved = save_learning(
                feature=feature,
                pattern=pattern,
                evidence_count=len(rows),
                average_performance=round(
                    performance,
                    2,
                ),
                metadata={
                    "average_views": round(
                        average_views,
                        2,
                    ),
                    "average_retention": round(
                        average_retention,
                        2,
                    ),
                },
            )
            new_learnings.append(saved)
        return {
            "success": True,
            "video_count": len(videos),
            "new_learnings": new_learnings,
        }
def learn_from_experiments():
    with _connect() as conn:
        _ensure_learning_table(conn)
        rows = conn.execute(
            """
            SELECT
                experiment_type,
                variant_name,
                result_metric,
                result_value,
                status
            FROM youtube_experiments
            WHERE result_value IS NOT NULL
            ORDER BY id ASC
            """
        ).fetchall()
        if not rows:
            return {
                "success": True,
                "experiment_count": 0,
                "new_learnings": [],
            }
        grouped = {}
        for row in rows:
            key = (
                str(row["experiment_type"]),
                str(row["result_metric"] or "unknown"),
            )
            grouped.setdefault(
                key,
                [],
            ).append(row)
        learnings = []
        for (
            experiment_type,
            result_metric,
        ), items in grouped.items():
            values = [
                float(item["result_value"])
                for item in items
            ]
            average_value = (
                sum(values) / len(values)
                if values
                else 0.0
            )
            best = max(
                items,
                key=lambda item: float(
                    item["result_value"]
                ),
            )
            pattern = (
                f"{experiment_type}: "
                f"{best['variant_name']}"
            )
            saved = save_learning(
                feature="experiment",
                pattern=pattern,
                evidence_count=len(items),
                average_performance=round(
                    average_value,
                    2,
                ),
                metadata={
                    "result_metric": result_metric,
                    "best_result": float(
                        best["result_value"]
                    ),
                    "best_variant": best["variant_name"],
                },
            )
            learnings.append(saved)
        return {
            "success": True,
            "experiment_count": len(rows),
            "new_learnings": learnings,
        }
def run_self_learning(
    channel_db_id: int,
):
    video_learning = learn_from_videos(
        channel_db_id
    )
    experiment_learning = (
        learn_from_experiments()
    )
    total_learnings = (
        len(video_learning["new_learnings"])
        + len(experiment_learning["new_learnings"])
    )
    return {
        "success": True,
        "channel_db_id": int(channel_db_id),
        "video_count": video_learning[
            "video_count"
        ],
        "experiment_count": experiment_learning[
            "experiment_count"
        ],
        "learning_count": total_learnings,
        "video_learning": video_learning,
        "experiment_learning": experiment_learning,
    }
def get_learning_summary():
    with _connect() as conn:
        _ensure_learning_table(conn)
        total = conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM youtube_learning
            """
        ).fetchone()["count"]
        high_confidence = conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM youtube_learning
            WHERE confidence >= 0.70
            """
        ).fetchone()["count"]
        features = conn.execute(
            """
            SELECT feature, COUNT(*) AS count
            FROM youtube_learning
            GROUP BY feature
            ORDER BY count DESC
            """
        ).fetchall()
        return {
            "success": True,
            "total_learnings": int(total),
            "high_confidence_learnings": int(
                high_confidence
            ),
            "features": [
                {
                    "feature": row["feature"],
                    "count": int(row["count"]),
                }
                for row in features
            ],
        }
class YouTubeSelfLearning:
    def save(
        self,
        feature: str,
        pattern: str,
        evidence_count: int = 1,
        average_performance: Optional[float] = None,
        confidence: Optional[float] = None,
        metadata: Optional[dict] = None,
    ):
        return save_learning(
            feature,
            pattern,
            evidence_count,
            average_performance,
            confidence,
            metadata,
        )
    def get(
        self,
        feature: Optional[str] = None,
        limit: int = 100,
    ):
        return get_learnings(
            feature,
            limit,
        )
    def learn_videos(
        self,
        channel_db_id: int,
    ):
        return learn_from_videos(
            channel_db_id
        )
    def learn_experiments(self):
        return learn_from_experiments()
    def learn(
        self,
        channel_db_id: int,
    ):
        return run_self_learning(
            channel_db_id
        )
    def summary(self):
        return get_learning_summary()
self_learning = YouTubeSelfLearning()
