import json
from database.connection import Database
from database.models import PredictionRecord
class PredictionRepository:
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
        record: PredictionRecord,
    ) -> int:
        with self.db.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO predictions (
                    question,
                    horizon_days,
                    prediction_json,
                    confidence
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    record.question,
                    record.horizon_days,
                    json.dumps(
                        record.prediction,
                        ensure_ascii=False,
                    ),
                    record.confidence,
                ),
            )
            conn.commit()
            return cursor.lastrowid
    def latest(
        self,
        limit: int = 20,
    ) -> list[dict]:
        with self.db.connect() as conn:
            rows = conn.execute(
                """
                SELECT
                    id,
                    question,
                    horizon_days,
                    prediction_json,
                    confidence,
                    created_at
                FROM predictions
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [
            {
                "id": row[0],
                "question": row[1],
                "horizon_days": row[2],
                "prediction": self._json(row[3]),
                "confidence": row[4],
                "created_at": row[5],
            }
            for row in rows
        ]
    @staticmethod
    def _json(value):
        try:
            return json.loads(value)
        except Exception:
            return {}
