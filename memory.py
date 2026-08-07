import json
from datetime import datetime

from database import Database


class MemorySystem:

    def __init__(self):

        self.db = Database()


    def remember(
        self,
        category,
        data
    ):

        created_at = datetime.now().isoformat()

        self.db.execute(
            """
            INSERT INTO memory
            (
                category,
                data,
                created_at
            )
            VALUES
            (?, ?, ?)
            """,
            (
                category,
                json.dumps(data),
                created_at
            )
        )

        return {
            "category": category,
            "data": data,
            "created_at": created_at
        }


    def recall(
        self,
        category=None
    ):

        if category:

            rows = self.db.execute(
                """
                SELECT
                    id,
                    category,
                    data,
                    created_at
                FROM memory
                WHERE category=?
                ORDER BY id
                """,
                (category,)
            ).fetchall()

        else:

            rows = self.db.execute(
                """
                SELECT
                    id,
                    category,
                    data,
                    created_at
                FROM memory
                ORDER BY id
                """
            ).fetchall()

        result = []

        for row in rows:

            result.append(
                {
                    "id": row[0],
                    "category": row[1],
                    "data": json.loads(row[2]),
                    "created_at": row[3]
                }
            )

        return result
