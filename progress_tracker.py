from datetime import datetime

from memory import MemorySystem


class ProgressTracker:

    def __init__(self):

        self.memory = MemorySystem()


    def start(
        self,
        goal,
        step
    ):

        return self.memory.remember(
            "progress",
            {
                "goal": goal,
                "step": step,
                "status": "started",
                "time": datetime.now().isoformat()
            }
        )


    def complete(
        self,
        goal,
        step
    ):

        return self.memory.remember(
            "progress",
            {
                "goal": goal,
                "step": step,
                "status": "completed",
                "time": datetime.now().isoformat()
            }
        )


    def get_progress(
        self,
        goal=None
    ):

        data = self.memory.recall("progress")

        if goal is None:
            return data

        return [
            item
            for item in data
            if item["data"].get("goal") == goal
        ]
