from datetime import datetime


class EvaluationEngine:

    def evaluate(self, job):

        score = 100

        return {
            "status": "success",
            "score": score,
            "improvement": [],
            "job": job,
            "time": datetime.now().isoformat()
        }
