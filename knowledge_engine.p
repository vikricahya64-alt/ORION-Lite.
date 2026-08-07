from database import Database
from datetime import datetime
import json


class KnowledgeEngine:

    def __init__(self):
        self.db = Database()


    def store_insight(self, insight):

        data = json.dumps(insight)


        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                created_at TEXT
            )
            """
        )


        self.db.execute(
            """
            INSERT INTO knowledge
            (data, created_at)
            VALUES (?, ?)
            """,
            (
                data,
                datetime.now().isoformat()
            )
        )


        return {
            "status": "stored",
            "knowledge": insight
        }


    def get_all(self):

        cursor = self.db.execute(
            """
            SELECT data, created_at
            FROM knowledge
            ORDER BY id DESC
            """
        )


        rows = cursor.fetchall()

        result = []


        for row in rows:

            result.append(
                {
                    "data": json.loads(row[0]),
                    "created_at": row[1]
                }
            )


        return {
            "total": len(result),
            "knowledge": result
        }
