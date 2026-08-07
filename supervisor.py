from datetime import datetime


class SupervisorAgent:


    def evaluate(self, job, result):

        score = 0


        # Eksekusi berhasil
        if result.get("executed"):

            score += 50


        # Action berhasil
        action = result.get(
            "action_result",
            {}
        )

        if action:

            score += 30


        # Tidak ada error
        if "error" not in result:

            score += 20



        if score >= 80:

            status = "good"
            recommendation = "Pertahankan metode"

        elif score >= 50:

            status = "medium"
            recommendation = "Optimasi metode"

        else:

            status = "bad"
            recommendation = "Perbaiki strategi"



        return {

            "score": score,

            "status": status,

            "recommendation":
            recommendation,

            "time":
            datetime.now().isoformat()

        }
