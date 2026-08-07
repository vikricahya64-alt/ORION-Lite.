from datetime import datetime


class AdaptiveLearning:

    def __init__(self):
        self.history = []


    def analyze(self, job):

        if not job:
            return {
                "status": "failed",
                "score": 0,
                "strategy": "Tidak ada data untuk dianalisis",
                "confidence": 0
            }


        # Ambil informasi job
        goal = job.get("goal", "Unknown")
        step = job.get("step", "Unknown")


        # Default hasil
        score = 0
        status = "unknown"
        strategy = "Ulangi analisis dengan pendekatan baru"
        confidence = 0.2


        # Evaluasi berdasarkan status eksekusi
        if job.get("status") == "completed":
            score = 100
            status = "success"
            strategy = "Pertahankan metode karena hasil optimal"
            confidence = 1.0


        # Simpan pengalaman adaptive learning
        record = {
            "goal": goal,
            "step": step,
            "score": score,
            "confidence": confidence,
            "time": datetime.utcnow().isoformat()
        }


        self.history.append(record)


        return {
            "status": status,
            "score": score,
            "strategy": strategy,
            "confidence": confidence
        }


    def history_log(self):

        return self.history
