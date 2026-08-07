import json
from database import Database


class MemoryCleaner:

    def __init__(self):
        self.db = Database()

    def clean_duplicates(self):
        rows = self.db.execute(
            """
            SELECT id, category, data, created_at
            FROM memories
            ORDER BY id ASC
            """
        )

        seen = set()
        removed = 0

        for row in rows:

            memory_id = row[0]
            category = row[1]
            data = row[2]

            key = (
                category,
                data
            )

            if key in seen:

                self.db.execute(
                    """
                    DELETE FROM memories
                    WHERE id = ?
                    """,
                    (memory_id,)
                )

                removed += 1

            else:
                seen.add(key)

        return {
            "status": "completed",
            "removed": removed,
            "remaining": len(seen)
        }


    def summarize(self):

        rows = self.db.execute(
            """
            SELECT category, COUNT(*)
            FROM memories
            GROUP BY category
            """
        )

        result = {}

        for row in rows:
            result[row[0]] = row[1]

        return {
            "total_categories": len(result),
            "summary": result
        }
