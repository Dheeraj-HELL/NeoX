import sqlite3
from datetime import datetime


class NeoXMemoryManager:
    """Manage persistent NeoX chat history using SQLite."""

    def __init__(self, db_name="neox_chat_history.db"):
        self.sqlite3 = sqlite3
        self.datetime = datetime
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                role TEXT,
                content TEXT
            )
            """
        )

        self.conn.commit()

    def save_message(self, role, content):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO chat_history (timestamp, role, content)
            VALUES (?, ?, ?)
            """,
            (
                self.datetime.now().isoformat(),
                role,
                content,
            ),
        )

        self.conn.commit()

    def load_history(self, limit=50):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT role, content
            FROM chat_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )

        return cursor.fetchall()[::-1]