from context_manager import ContextManager


class DecisionEngine:

    def __init__(self):

        self.context = ContextManager()


    def decide(self, goal):

        ctx = self.context.build(goal)

        action = "task"

        priority = 3

        reason = "Pekerjaan umum"


        text = goal.lower()


        if any(
            word in text
            for word in [
                "belajar",
                "pelajari",
                "mempelajari"
            ]
        ):

            action = "learning"

            priority = 4

            reason = "Pengembangan pengetahuan"


        elif any(
            word in text
            for word in [
                "buat",
                "bangun",
                "kerjakan"
            ]
        ):

            action = "task"

            priority = 5

            reason = "Eksekusi pekerjaan"


        return {

            "goal": goal,

            "action": action,

            "priority": priority,

            "reason": reason,

            "context": ctx

        }
