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
            # Persistent user memory
            # --------------------------------------------------------
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    memory_key TEXT NOT NULL,
                    memory_value TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(user_id, memory_key)
                )
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_memory_user_id
                ON memory(user_id)
            ''')


            # --------------------------------------------------------
            # Central cross-device chat history
            # --------------------------------------------------------
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')



            # Add chat_id column for separate conversations
            cursor.execute(
                "PRAGMA table_info(chat_history)"
            )

            chat_history_columns = {
                row[1]
                for row in cursor.fetchall()
            }

            if "chat_id" not in chat_history_columns:

                cursor.execute(
                    """
                    ALTER TABLE chat_history
                    ADD COLUMN chat_id TEXT
                    """
                )

                cursor.execute(
                    """
                    UPDATE chat_history
                    SET chat_id = 'legacy'
                    WHERE chat_id IS NULL
                    """
                )





            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_chat_history_user_id
                ON chat_history(user_id)
            ''')



            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_chat_history_user_chat_id
                ON chat_history(user_id, chat_id)
            ''')





            # --------------------------------------------------------



            # --------------------------------------------------------
            # Central user accounts for cross-device sync
            # --------------------------------------------------------
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL UNIQUE,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_users_user_id
                ON users(user_id)
            ''')
            # --------------------------------------------------------



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

    def save_memory(self, user_id: str, memory_key: str, memory_value: str) -> bool:
        user_id = str(user_id).strip()
        memory_key = str(memory_key).strip().lower()
        memory_value = str(memory_value).strip()

        if not user_id or not memory_key or not memory_value:
            return False

        now_str = datetime.now(timezone.utc).isoformat()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO memory
                (user_id, memory_key, memory_value, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id, memory_key) DO UPDATE SET
                    memory_value=excluded.memory_value,
                    updated_at=excluded.updated_at
            ''', (
                user_id,
                memory_key,
                memory_value,
                now_str,
                now_str,
            ))
            conn.commit()

        return True


    def get_memories(self, user_id: str) -> Dict[str, str]:
        user_id = str(user_id).strip()

        if not user_id:
            return {}

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT memory_key, memory_value
                FROM memory
                WHERE user_id = ?
                ORDER BY updated_at DESC
            ''', (user_id,))

            rows = cursor.fetchall()

        return {
            str(memory_key): str(memory_value)
            for memory_key, memory_value in rows
        }

    def save_chat_message(
        self,
        user_id: str,
        chat_id: str,
        role: str,
        message: str,
    ) -> bool:


        
        user_id = str(user_id).strip()
        chat_id = str(chat_id).strip()
        role = str(role).strip().lower()
        message = str(message).strip()

        if (
            not user_id
            or not chat_id
            or role not in {"user", "assistant"}
            or not message
        ):
            return False

        created_at = datetime.now(timezone.utc).isoformat()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO chat_history
                (user_id, chat_id, role, message, created_at)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (
                    user_id,
                    chat_id,
                    role,
                    message,
                    created_at,
                ),
            )
            conn.commit()

        return True

    def get_chat_history(
        self,
        user_id: str,
        chat_id: str,
    ) -> list[Dict[str, str]]:

        
        user_id = str(user_id).strip()
        chat_id = str(chat_id).strip()

        if not user_id or not chat_id:
            return []

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT role, message, created_at
                FROM chat_history
                WHERE user_id = ?
                AND chat_id = ?
                ORDER BY id ASC
                ''',
                (
                    user_id,
                    chat_id,
                ),
            )

            rows = cursor.fetchall()

        return [
            {
                "role": str(role),
                "message": str(message),
                "created_at": str(created_at),
            }
            for role, message, created_at in rows
        ]

    def clear_chat_history(self, user_id: str) -> bool:
        user_id = str(user_id).strip()

        if not user_id:
            return False

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                DELETE FROM chat_history
                WHERE user_id = ?
                ''',
                (user_id,),
            )
            conn.commit()

        return True



    # --------------------------------------------------------
    # Central user account methods
    # --------------------------------------------------------
    def create_user_account(
        self,
        user_id: str,
        username: str,
        password_hash: str,
    ) -> bool:
        user_id = str(user_id).strip()
        username = str(username).strip().lower()
        password_hash = str(password_hash).strip()

        if not user_id or not username or not password_hash:
            return False

        created_at = datetime.now(timezone.utc).isoformat()

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    INSERT INTO users
                    (user_id, username, password_hash, created_at)
                    VALUES (?, ?, ?, ?)
                    ''',
                    (
                        user_id,
                        username,
                        password_hash,
                        created_at,
                    ),
                )
                conn.commit()

            return True

        except sqlite3.IntegrityError:
            return False

    def get_user_account(
        self,
        username: str,
    ) -> Optional[Dict[str, str]]:
        username = str(username).strip().lower()

        if not username:
            return None

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT user_id, username, password_hash, created_at
                FROM users
                WHERE username = ?
                LIMIT 1
                ''',
                (username,),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return {
            "user_id": str(row[0]),
            "username": str(row[1]),
            "password_hash": str(row[2]),
            "created_at": str(row[3]),
        }

    



