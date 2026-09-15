import sqlite3
from pathlib import Path
class Database:
    def __init__(
        self,
        path: str = "data/ismail.db",
    ):
        self.path = Path(path)
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
    def connect(self):
        return sqlite3.connect(
            self.path,
            check_same_thread=False,
        )
    def initialize(self):
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS
                historical_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    value TEXT NOT NULL,
                    source TEXT,
                    source_type TEXT,
                    timestamp TEXT NOT NULL,
                    reliability REAL DEFAULT 0.5,
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_historical_topic
                ON historical_data(topic)
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_historical_timestamp
                ON historical_data(timestamp)
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS
                predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    horizon_days INTEGER NOT NULL,
                    prediction_json TEXT NOT NULL,
                    confidence REAL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_predictions_created
                ON predictions(created_at)
                """
            )
            conn.commit()
