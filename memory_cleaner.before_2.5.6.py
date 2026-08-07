import json

from database import Database
from optimizer import DatabaseOptimizer


class MemoryCleaner:

    def __init__(self):

        self.db = Database()

        self.optimizer = DatabaseOptimizer()


    def stats(self):

        rows = self.db.execute(

            """
            SELECT category,
                   COUNT(*)
            FROM memory
            GROUP BY category
            """

        ).fetchall()

        result = {}

        total = 0

        for row in rows:

            result[row[0]] = row[1]

            total += row[1]

        return {

            "total": total,

            "categories": result

        }


    def remove_duplicate_memory(self):

        rows = self.db.execute(

            """
            SELECT
                id,
                category,
                data

            FROM memory

            ORDER BY id ASC
            """

        ).fetchall()

        seen = set()

        removed = 0

        for row in rows:

            key = (

                row[1],

                row[2]

            )

            if key in seen:

                self.db.execute(

                    """
                    DELETE FROM memory
                    WHERE id=?
                    """,

                    (row[0],)

                )

                removed += 1

            else:

                seen.add(key)

        return {

            "removed_duplicates": removed

        }


    def remove_old_progress(self, keep_latest=100):

        rows = self.db.execute(

            """
            SELECT id

            FROM memory

            WHERE category='progress'

            ORDER BY id DESC
            """

        ).fetchall()

        if len(rows) <= keep_latest:

            return {

                "removed_progress": 0

            }

        deleted = 0

        for row in rows[keep_latest:]:

            self.db.execute(

                """
                DELETE FROM memory
                WHERE id=?
                """,

                (row[0],)

            )

            deleted += 1

        return {

            "removed_progress": deleted

        }


    def summarize_learning(self):

        rows = self.db.execute(

            """
            SELECT data

            FROM memory

            WHERE category='learning'
            """

        ).fetchall()

        topics = {}

        for row in rows:

            try:

                data = json.loads(row[0])

            except Exception:

                continue

            topic = data.get(

                "topic",

                "unknown"

            )

            topics[topic] = topics.get(

                topic,

                0

            ) + 1

        return {

            "learning_topics": topics,

            "total_topics": len(topics)

        }


    def optimize(self):

        duplicate = self.remove_duplicate_memory()

        progress = self.remove_old_progress()

        summary = self.summarize_learning()

        database = self.optimizer.optimize()

        return {

            "status": "completed",

            "duplicates": duplicate,

            "progress": progress,

            "summary": summary,

            "database": database

        }
