import json
from database.connection import Database
from database.models import HistoricalRecord
class HistoricalRepository:
    def __init__(
        self,
        database: Database | None = None,
    ):
        self.db = (
            database
            or Database()
        )
        self.db.initialize()
    def insert(
        self,
        record: HistoricalRecord,
    ) -> int:
        with self.db.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO historical_data (
                    topic,
                    value,
                    source,
                    source_type,
                    timestamp,
                    reliability,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.topic,
                    record.value,
                    record.source,
                    record.source_type,
                    record.timestamp,
                    record.reliability,
                    json.dumps(
                        record.metadata,
                        ensure_ascii=False,
                    ),
                ),
            )
            conn.commit()
            return cursor.lastrowid
    def list_by_topic(
        self,
        topic: str,
        limit: int = 100,
    ) -> list[dict]:
        with self.db.connect() as conn:
            rows = conn.execute(
                """
                SELECT
                    id,
                    topic,
                    value,
                    source,
                    source_type,
                    timestamp,
                    reliability,
                    metadata,
                    created_at
                FROM historical_data
                WHERE topic = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (
                    topic,
                    limit,
                ),
            ).fetchall()
        return [
            {
                "id": row[0],
                "topic": row[1],
                "value": row[2],
                "source": row[3],
                "source_type": row[4],
                "timestamp": row[5],
                "reliability": row[6],
                "metadata": self._json(row[7]),
                "created_at": row[8],
            }
            for row in rows
        ]
    def count(
        self,
        topic: str | None = None,
    ) -> int:
        with self.db.connect() as conn:
            if topic:
                row = conn.execute(
                    """
                    SELECT COUNT(*)
                    FROM historical_data
                    WHERE topic = ?
                    """,
                    (topic,),
                ).fetchone()
            else:
                row = conn.execute(
                    """
                    SELECT COUNT(*)
                    FROM historical_data
                    """
                ).fetchone()
        return int(row[0])
    @staticmethod
    def _json(value):
        try:
            return json.loads(value)
        except Exception:
            return {}
