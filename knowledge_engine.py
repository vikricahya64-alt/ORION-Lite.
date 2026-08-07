from database import Database
from datetime import datetime
import json


class KnowledgeEngine:

    def __init__(self):
        self.db = Database()


        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                data TEXT,
                created_at TEXT
            )
            """
        )


    def store_insight(self, insight):

        topic = insight.get(
            "category",
            "general"
        )

        data = json.dumps(insight)


        self.db.execute(
            """
            INSERT INTO knowledge
            (
                topic,
                data,
                created_at
            )
            VALUES (?, ?, ?)
            """,
            (
                topic,
                data,
                datetime.now().isoformat()
            )
        )


        return {
            "status": "stored",
            "topic": topic,
            "data": insight
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



    # kompatibilitas ORION lama

    def learn(self, topic, data):

        return self.store_insight(
            {
                "category": topic,
                "content": data
            }
        )


    def search(self, keyword):

        cursor = self.db.execute(
            """
            SELECT data
            FROM knowledge
            WHERE data LIKE ?
            """,
            (
                f"%{keyword}%",
            )
        )

        rows = cursor.fetchall()


        return [
            json.loads(row[0])
            for row in rows
        ]



    def topics(self):

        cursor = self.db.execute(
            """
            SELECT DISTINCT topic
            FROM knowledge
            """
        )

        return [
            row[0]
            for row in cursor.fetchall()
        ]



    def statistics(self):

        cursor = self.db.execute(
            """
            SELECT COUNT(*)
            FROM knowledge
            """
        )

        total = cursor.fetchone()[0]

        return {
            "total_knowledge": total
        }
