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

        job = data.get("job", {})

        goal = job.get("goal")

        if not goal:
            goal = "Unknown Goal"


        # Evaluasi hasil kerja
        evaluation_result = self.evaluation.evaluate(
            job
        )


        # Adaptive learning hanya menerima job
        adaptive_result = self.adaptive.analyze(
            job
        )


        # Simpan pengalaman
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
                )
            }
        )


        # Refleksi pengalaman
        reflection_result = self.reflection.reflect(
            goal
        )


        return {
            "evaluation": evaluation_result,
            "adaptive_learning": adaptive_result,
            "memory": memory_result,
            "reflection": reflection_result
        }
