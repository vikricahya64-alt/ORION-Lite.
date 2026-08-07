from datetime import datetime

from evaluation import EvaluationEngine
from adaptive_learning import AdaptiveLearning
from memory import MemorySystem
from reflection import ReflectionEngine
from self_improvement import SelfImprovement


class EventHandlers:

    def __init__(self):
        self.evaluation = EvaluationEngine()
        self.adaptive = AdaptiveLearning()
        self.memory = MemorySystem()
        self.reflection = ReflectionEngine()
        self.self_improvement = SelfImprovement()


    def handle_job_completed(self, job):

        data = job.get("data", {})

        # Evaluation Engine
        evaluation_result = self.evaluation.evaluate(
            data
        )


        # Adaptive Learning
        adaptive_result = self.adaptive.analyze(
            evaluation_result
        )


        # Memory System
        memory_data = {
            "goal": data.get(
                "goal",
                "Unknown Goal"
            ),
            "decision": {
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
        }


        try:
            if hasattr(self.memory, "store"):

                memory_result = self.memory.store(
                    "decision",
                    memory_data
                )

            elif hasattr(self.memory, "save"):

                memory_result = self.memory.save(
                    "decision",
                    memory_data
                )

            else:

                memory_result = {
                    "status": "skipped",
                    "reason": "memory method unavailable"
                }

        except Exception as e:

            memory_result = {
                "status": "error",
                "message": str(e)
            }


        # Reflection Engine
        try:

            reflection_result = self.reflection.analyze(
                data.get(
                    "goal",
                    "Unknown Goal"
                )
            )

        except Exception as e:

            reflection_result = {
                "status": "error",
                "message": str(e)
            }


        # Self Improvement
        try:

            improvement_result = self.self_improvement.analyze(
                evaluation_result
            )

        except Exception as e:

            improvement_result = {
                "status": "error",
                "message": str(e)
            }


        return {
            "event": "job_completed",
            "time": datetime.now().isoformat(),
            "evaluation": evaluation_result,
            "adaptive_learning": adaptive_result,
            "memory": memory_result,
            "reflection": reflection_result,
            "self_improvement": improvement_result
        }


    # Dipanggil langsung oleh worker.py
    # JANGAN dibuat async
    def job_completed(self, job):

        return self.handle_job_completed(job)


    def handle(self, event, job):

        if event == "job_completed":

            return self.handle_job_completed(job)


        return {
            "status": "ignored",
            "event": event
        }
