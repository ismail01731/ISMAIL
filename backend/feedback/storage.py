from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
class FeedbackStorage:
    def __init__(
        self,
        db_path: Optional[str] = None,
    ):
        if db_path is None:
            db_path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "ismail.db"
            )
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        self._create_table()
    def _connect(self):
        return sqlite3.connect(
            self.db_path
        )
    def _create_table(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS
                prediction_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prediction_id INTEGER,
                    predicted_value REAL NOT NULL,
                    actual_value REAL NOT NULL,
                    confidence REAL NOT NULL,
                    absolute_error REAL NOT NULL,
                    percentage_error REAL NOT NULL,
                    directional_accuracy INTEGER NOT NULL,
                    notes TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()
    def insert(
        self,
        feedback: Dict,
    ) -> int:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO prediction_feedback (
                    prediction_id,
                    predicted_value,
                    actual_value,
                    confidence,
                    absolute_error,
                    percentage_error,
                    directional_accuracy,
                    notes,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    feedback.get("prediction_id"),
                    feedback["predicted_value"],
                    feedback["actual_value"],
                    feedback["confidence"],
                    feedback["absolute_error"],
                    feedback["percentage_error"],
                    int(
                        feedback["directional_accuracy"]
                    ),
                    feedback.get("notes"),
                    feedback["created_at"],
                ),
            )
            conn.commit()
            return cursor.lastrowid
    def list_all(self) -> List[Dict]:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT
                    id,
                    prediction_id,
                    predicted_value,
                    actual_value,
                    confidence,
                    absolute_error,
                    percentage_error,
                    directional_accuracy,
                    notes,
                    created_at
                FROM prediction_feedback
                ORDER BY id DESC
                """
            )
            rows = cursor.fetchall()
        columns = [
            "id",
            "prediction_id",
            "predicted_value",
            "actual_value",
            "confidence",
            "absolute_error",
            "percentage_error",
            "directional_accuracy",
            "notes",
            "created_at",
        ]
        return [
            dict(zip(columns, row))
            for row in rows
        ]
