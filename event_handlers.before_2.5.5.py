from evaluation import EvaluationEngine
from adaptive_learning import AdaptiveLearning
from decision_memory import DecisionMemory
from reflection import ReflectionEngine


class EventHandlers:

    def __init__(self):
        self.evaluation = EvaluationEngine()
        self.adaptive = AdaptiveLearning()
        self.memory = DecisionMemory()
        self.reflection = ReflectionEngine()


    def job_completed(self, data):

        # Ambil job dari event
        job = data.get("job", {})


        # Support berbagai format data worker
        job_data = job.get(
            "data",
            job
        )


        goal = job_data.get(
            "goal",
            job.get(
                "goal",
                "Unknown Goal"
            )
        )


        step = job_data.get(
            "step",
            job.get(
                "step",
                "Unknown Step"
            )
        )


        priority = job_data.get(
            "priority",
            job.get(
                "priority",
                0
            )
        )


        # Normalisasi job
        normalized_job = {
            "goal": goal,
            "step": step,
            "priority": priority,
            "status": "completed"
        }


        # =========================
        # 1. Evaluation Engine
        # =========================

        evaluation_result = self.evaluation.evaluate(
            normalized_job
        )


        # =========================
        # 2. Adaptive Learning
        # =========================

        adaptive_result = self.adaptive.analyze(
            {
                **normalized_job,
                "evaluation": evaluation_result
            }
        )


        # =========================
        # 3. Decision Memory
        # =========================

        memory_result = self.memory.record(
            goal,
            {
                "score": evaluation_result.get(
                    "score",
                    0
                ),
                "confidence": adaptive_result.get(
                    "confidence",
                    0
                ),
                "strategy": adaptive_result.get(
                    "strategy",
                    ""
                )
            }
        )


        # =========================
        # 4. Reflection Engine
        # =========================

        reflection_result = self.reflection.reflect(
            goal
        )


        return {
            "evaluation": evaluation_result,
            "adaptive_learning": adaptive_result,
            "memory": memory_result,
            "reflection": reflection_result
        }
