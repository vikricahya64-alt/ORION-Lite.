from decision_memory import DecisionMemory
from context_manager import ContextManager


class DecisionEngine:

    def __init__(self):
        self.memory = DecisionMemory()
        self.context = ContextManager()


    def decide(self, goal):

        context_data = self.context.build_context(goal)

        success_rate = self.memory.success_rate(goal)


        action = "learning"
        priority = 5
        confidence = 0.5
        strategy = "Mulai analisis baru"


        if success_rate >= 0.8:

            action = "learning"
            priority = 4
            confidence = 1.0
            strategy = "Gunakan strategi sebelumnya yang berhasil"


        elif success_rate == 0:

            action = "learning"
            priority = 5
            confidence = 0.5
            strategy = "Eksplorasi pendekatan baru"


        else:

            action = "review"
            priority = 6
            confidence = 0.6
            strategy = "Evaluasi ulang strategi"


        return {
            "goal": goal,
            "action": action,
            "priority": priority,
            "confidence": confidence,
            "strategy": strategy,
            "success_rate": success_rate,
            "context": context_data
        }
