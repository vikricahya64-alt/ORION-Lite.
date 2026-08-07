from database import Database
from knowledge_engine import KnowledgeEngine
from datetime import datetime


class MemoryConsolidator:

    def __init__(self):
        self.db = Database()
        self.knowledge = KnowledgeEngine()


    def consolidate(self):

        cursor = self.db.execute(
            """
            SELECT data
            FROM memories
            WHERE category = ?
            """,
            ("decision",)
        )

        rows = cursor.fetchall()


        if not rows:
            return {
                "status": "empty",
                "message": "Tidak ada memory untuk dikonsolidasi"
            }


        total = len(rows)

        scores = []
        goals = []


        for row in rows:

            data = row[0]

            if isinstance(data, str):
                text = data
            else:
                text = str(data)


            if "score" in text:
                scores.append(100)


            if "Belajar membuat AI Agent" in text:
                goals.append(
                    "Belajar membuat AI Agent"
                )


        average_score = (
            sum(scores) / len(scores)
            if scores
            else 0
        )


        insight = {
            "category": "decision",
            "memory_total": total,
            "average_score": average_score,
            "common_goals": list(set(goals)),
            "generated_at": datetime.now().isoformat()
        }


        # simpan hasil konsolidasi ke knowledge
        knowledge_result = self.knowledge.store_insight(
            insight
        )


        return {
            "status": "completed",
            "insight": insight,
            "knowledge": knowledge_result
        }
