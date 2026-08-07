from app.llm import LLMClient


class PlannerAgent:

    def __init__(self):

        self.name = "ORION Planner"
        self.llm = LLMClient()
    def create_plan(self, goal):

        # ==========================
        # Coba gunakan LLM terlebih dahulu
        # ==========================
        try:

            if hasattr(self.llm, "planner"):

                plan = self.llm.planner(goal)

                if isinstance(plan, dict):

                    steps = plan.get("steps") or plan.get("tasks")

                    if isinstance(steps, list) and len(steps) > 0:

                        return {
                            "goal": goal,
                            "steps": steps,
                            "total_steps": len(steps)
                        }

        except Exception:
            pass

        # ==========================
        # Fallback jika LLM gagal
        # ==========================

        goal_lower = goal.lower()

        if "belajar" in goal_lower:

            steps = [
                "Pelajari konsep dasar",
                "Kumpulkan informasi",
                "Praktikkan materi",
                "Evaluasi hasil belajar"
            ]

        elif "buat" in goal_lower or "membangun" in goal_lower:

            steps = [
                "Analisis kebutuhan",
                "Rancang solusi",
                "Implementasikan sistem",
                "Uji hasil"
            ]

        else:

            steps = [
                "Analisis tujuan",
                "Tentukan tindakan",
                "Jalankan pekerjaan"
            ]

        return {
            "goal": goal,
            "steps": steps,
            "total_steps": len(steps)
        }
