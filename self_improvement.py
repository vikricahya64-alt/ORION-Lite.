from datetime import datetime


class SelfImprovement:

    def __init__(self):
        self.history = []


    def analyze(self, evaluation, reflection=None):

        score = evaluation.get("score", 0)

        strategy = "Pertahankan strategi"

        confidence = 0.5

        status = "review"


        if score >= 90:
            status = "optimized"
            strategy = "Strategi berhasil, gunakan kembali"
            confidence = 1.0

        elif score >= 70:
            status = "stable"
            strategy = "Strategi cukup baik, lakukan penyempurnaan"
            confidence = 0.7

        else:
            status = "improve"
            strategy = "Ganti pendekatan dan lakukan evaluasi ulang"
            confidence = 0.4


        result = {
            "status": status,
            "score": score,
            "strategy": strategy,
            "confidence": confidence,
            "reflection_used": reflection is not None,
            "generated_at": datetime.now().isoformat()
        }


        self.history.append(result)

        return result


    def get_history(self):

        return {
            "total": len(self.history),
            "history": self.history
        }


    def recommend(self):

        if not self.history:
            return {
                "recommendation": "Belum ada data pembelajaran"
            }


        latest = self.history[-1]


        return {
            "recommendation": latest["strategy"],
            "confidence": latest["confidence"]
        }
