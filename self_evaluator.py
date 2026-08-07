class SelfEvaluator:


    def __init__(self):

        self.name = "ORION Self Evaluator"



    def evaluate(self, job, result):

        score = 0

        status = "failed"

        improvement = []


        if result:

            score += 50


        if isinstance(result, dict):

            if result.get("executed"):

                score += 30


            if result.get("type"):

                score += 20



        if score >= 80:

            status = "success"

        elif score >= 50:

            status = "partial"

        else:

            status = "failed"



        if status != "success":

            improvement.append(
                "Perlu peningkatan kualitas hasil"
            )


        return {

            "status": status,

            "score": score,

            "improvement": improvement,

            "job": job

        }
