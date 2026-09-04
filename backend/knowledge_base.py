import sqlite3
import os
import re
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from backend.freshness import FreshnessEngine
class KnowledgeBase:
    def __init__(self, db_path: str = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, "data", "knowledge.db")
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.initialize()
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    def normalize_question(self, question: str) -> str:
        if not question:
            return ""
        q = question.lower().strip()
        q = re.sub(r'[^\w\s]', '', q)
        q = re.sub(r'\s+', ' ', q)
        return q


    def initialize(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    normalized_question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    topic TEXT,
                    source TEXT,
                    source_url TEXT,
                    verified INTEGER DEFAULT 0,
                    confidence REAL DEFAULT 0.0,
                    created_at TEXT NOT NULL,
                    expires_at TEXT,
                    knowledge_type TEXT DEFAULT 'permanent'
                )
            ''')
            
            # --- [নতুন যোগ করার কাস্টম লাইনগুলো এখানে বসবে] ---
            # Migration check: Ensure UNIQUE index exists for ON CONFLICT
            cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_normalized_question ON knowledge(normalized_question);")

            # Migration check: Ensure knowledge_type column exists
            cursor.execute("PRAGMA table_info(knowledge)")
            columns = [info[1] for info in cursor.fetchall()]
            if 'knowledge_type' not in columns:
                cursor.execute("ALTER TABLE knowledge ADD COLUMN knowledge_type TEXT DEFAULT 'permanent'")
            # --------------------------------------------------------
            
            
            conn.commit()


    def save(self, question: str, answer: str, topic: str = None, 
             source: str = None, source_url: str = None, verified: bool = False, 
             confidence: float = 0.0, expires_at: Optional[str] = None, 
             knowledge_type: str = "permanent") -> bool:
        norm_q = self.normalize_question(question)
        if not norm_q:
            return False
        now_str = datetime.now(timezone.utc).isoformat()
        # If expires_at is not explicitly provided, calculate using FreshnessEngine
        if expires_at is None and knowledge_type != "permanent":
            expires_at = FreshnessEngine.calculate_expiry(topic=topic or question, knowledge_type=knowledge_type)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO knowledge 
                (question, normalized_question, answer, topic, source, source_url, verified, confidence, created_at, expires_at, type, knowledge_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(normalized_question) DO UPDATE SET
                    question=excluded.question,
                    answer=excluded.answer,
                    topic=excluded.topic,
                    source=excluded.source,
                    source_url=excluded.source_url,
                    verified=excluded.verified,
                    confidence=excluded.confidence,
                    created_at=excluded.created_at,
                    expires_at=excluded.expires_at,
                    type=excluded.type,
                    knowledge_type=excluded.knowledge_type
            ''', (question, norm_q, answer, topic, source, source_url, 1 if verified else 0, confidence, now_str, expires_at, knowledge_type, knowledge_type))
            conn.commit()
            return int(cursor.lastrowid)
    def get(self, question: str, knowledge_type: Optional[str] = None) -> Optional[Dict[str, Any]]:
        norm_q = self.normalize_question(question)
        if not norm_q:
            return None
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if knowledge_type:
                cursor.execute('''
                    SELECT * FROM knowledge
                    WHERE normalized_question = ?
                      AND (
                          expires_at IS NULL
                          OR expires_at > ?
                      )
                      AND knowledge_type = ?
                    ORDER BY verified DESC, created_at DESC
                    LIMIT 1
                ''', (norm_q, datetime.now(timezone.utc).isoformat(), knowledge_type))
            else:
                cursor.execute('''
                    SELECT * FROM knowledge
                    WHERE normalized_question = ?
                      AND (
                          expires_at IS NULL
                          OR expires_at > ?
                      )
                    ORDER BY verified DESC, created_at DESC
                    LIMIT 1
                ''', (norm_q, datetime.now(timezone.utc).isoformat()))
            row = cursor.fetchone()
            if not row:
                return None
            res = dict(row)
            # Expiry validation check
            expires_at = res.get("expires_at")
            if expires_at:
                try:
                    exp_dt = datetime.fromisoformat(expires_at)
                    now_dt = datetime.now(timezone.utc)
                    if exp_dt.tzinfo is None:
                        exp_dt = exp_dt.replace(tzinfo=timezone.utc)
                    if now_dt >= exp_dt:
                        return None  # Knowledge has expired
                except ValueError:
                    pass
            return res
    def count(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM knowledge')
            return cursor.fetchone()[0]
    def clear(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM knowledge')
            conn.commit()



