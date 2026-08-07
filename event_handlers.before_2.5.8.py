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

        # Ambil data pekerjaan
        job_data = job.get("data", {})

        goal = job_data.get(
            "goal",
            "Unknown Goal"
        )

        step = job_data.get(
            "step",
            "Unknown Step"
        )


        # Normalisasi data untuk engine
        normalized_job = {
            "goal": goal,
            "step": step,
            "priority": job_data.get(
                "priority",
                0
            ),
            "status": "completed"
        }


        # 1. Evaluasi pekerjaan
        evaluation_result = self.evaluation.evaluate(
            normalized_job
        )


        # 2. Adaptive Learning membaca hasil evaluasi
        adaptive_input = {
            **normalized_job,
            "evaluation": evaluation_result
        }


        adaptive_result = self.adaptive.analyze(
            adaptive_input
        )


        # 3. Simpan keputusan/pengalaman
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


        # 4. Refleksi
        reflection_result = self.reflection.reflect(
            goal
        )


        return {
            "evaluation": evaluation_result,
            "adaptive_learning": adaptive_result,
            "memory": memory_result,
            "reflection": reflection_result
        }
