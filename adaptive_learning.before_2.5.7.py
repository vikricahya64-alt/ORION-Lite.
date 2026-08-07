class AdaptiveLearning:


    def __init__(self):

        self.name = "ORION Adaptive Learning"



    def analyze(self, evaluation):


        score = evaluation.get(
            "score",
            0
        )


        status = evaluation.get(
            "status",
            "unknown"
        )


        strategy = ""


        confidence = 0



        if status == "success":

            strategy = (
                "Pertahankan metode "
                "karena hasil optimal"
            )

            confidence = 1.0



        elif status == "partial":

            strategy = (
                "Perbaiki langkah "
                "yang menghasilkan nilai rendah"
            )

            confidence = 0.5



        else:

            strategy = (
                "Ulangi analisis "
                "dengan pendekatan baru"
            )

            confidence = 0.2



        return {

            "status": status,

            "score": score,

            "strategy": strategy,

            "confidence": confidence

        }
