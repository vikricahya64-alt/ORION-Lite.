from datetime import datetime


class ReflectionEngine:

    def __init__(self, memory=None):
        self.memory = memory


    def reflect(self, goal):

        reflection = {
            "goal": goal,
            "time": datetime.now().isoformat(),
            "analysis": {},
            "recommendation": []
        }


        if self.memory:

            history = self.memory.history()

            related = [
                item for item in history
                if goal in str(item)
            ]

            reflection["analysis"]["memory_count"] = len(related)


            if len(related) > 3:
                reflection["recommendation"].append(
                    "Gunakan strategi lama karena pengalaman cukup"
                )

            else:
                reflection["recommendation"].append(
                    "Kumpulkan lebih banyak pengalaman"
                )


        else:
            reflection["analysis"]["memory_count"] = 0


        return reflection
