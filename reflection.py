from datetime import datetime

from decision_memory import DecisionMemory


class ReflectionEngine:
    def __init__(self):
        self.memory = DecisionMemory()

    def reflect(self, goal):
        if not goal:
            goal = "Unknown Goal"

        history = self.memory.history()

        related = []

        for item in history:
            data = item.get("data", {})

            item_goal = data.get("goal")

            if item_goal == goal:
                related.append(item)

        recommendations = []

        if len(related) == 0:
            recommendations.append(
                "Belum ada pengalaman sebelumnya, gunakan strategi eksplorasi."
            )

        else:
            success = self.memory.success_rate(goal)

            if success >= 0.8:
                recommendations.append(
                    "Strategi sebelumnya efektif, pertahankan pendekatan."
                )
            else:
                recommendations.append(
                    "Evaluasi ulang strategi karena hasil belum optimal."
                )

        return {
            "goal": goal,
            "time": datetime.now().isoformat(),
            "analysis": {
                "memory_count": len(related),
                "success_rate": self.memory.success_rate(goal)
            },
            "recommendation": recommendations
        }
