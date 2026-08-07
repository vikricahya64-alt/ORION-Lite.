from knowledge_engine import KnowledgeEngine
from decision_memory import DecisionMemory
from datetime import datetime


class ContextManager:
    def __init__(self):
        self.knowledge = KnowledgeEngine()
        self.memory = DecisionMemory()

    def build_context(self, goal):
        """
        Mengambil konteks sebelum ORION mengambil keputusan.
        """

        knowledge_result = self.knowledge.search(goal)

        memory_result = self.memory.history()

        related_memory = []

        for item in memory_result:
            data = item.get("data", {})

            if goal.lower() in str(data).lower():
                related_memory.append(data)

        return {
            "goal": goal,
            "timestamp": datetime.now().isoformat(),

            "knowledge": knowledge_result,

            "memory": {
                "total": len(memory_result),
                "related": related_memory
            },

            "context_ready": True
        }


    def get_context(self, goal):
        """
        Alias agar kompatibel dengan modul lain.
        """
        return self.build_context(goal)


    def summarize(self, goal):
        """
        Ringkasan konteks untuk Decision Engine.
        """

        context = self.build_context(goal)

        return {
            "goal": goal,
            "knowledge_found": context["knowledge"].get(
                "total", 0
            ) if isinstance(context["knowledge"], dict) else 0,

            "memory_found": len(
                context["memory"]["related"]
            ),

            "ready": True
        }
