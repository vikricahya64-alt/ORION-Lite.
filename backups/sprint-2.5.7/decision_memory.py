import json
from datetime import datetime

from database import Database


class DecisionMemory:
    def __init__(self):
        self.db = Database()

        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                data TEXT,
                created_at TEXT
            )
            """
        )

    def record(self, goal, decision):
        payload = {
            "goal": goal,
            "decision": decision
        }

        self.db.execute(
            """
            INSERT INTO memories
            (category, data, created_at)
            VALUES (?, ?, ?)
            """,
            (
                "decision",
                json.dumps(payload),
                datetime.now().isoformat()
            )
        )

        return {
            "category": "decision",
            "data": payload,
            "created_at": datetime.now().isoformat()
        }

    def history(self):
        rows = self.db.execute(
            """
            SELECT id, category, data, created_at
            FROM memories
            WHERE category = ?
            ORDER BY id ASC
            """,
            ("decision",)
        )

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

    def success_rate(self, goal):
        history = self.history()

        scores = []

        for item in history:
            data = item.get("data", {})

            if data.get("goal") != goal:
                continue

            decision = data.get("decision", {})

            score = decision.get("score")

            if isinstance(score, (int, float)):
                scores.append(score)

        if not scores:
            return 0.0

        success = [
            score
            for score in scores
            if score >= 80
        ]

        return round(
            len(success) / len(scores),
            2
        )

    def best_decision(self, goal):
        history = self.history()

        best = None

        for item in history:
            data = item.get("data", {})

            if data.get("goal") != goal:
                continue

            decision = data.get("decision", {})

            score = decision.get("score")

            if isinstance(score, (int, float)):

                if best is None or score > best["score"]:
                    best = {
                        "score": score,
                        "decision": decision
                    }

        return best
