from datetime import datetime



class AdaptiveLearning:


    def __init__(self, memory=None):

        self.memory = memory

        self.history = []



    # ==========================
    # ANALYZE EXPERIENCE
    # ==========================

    def analyze(self, job):


        if not job:


            return {

                "status": "failed",

                "score": 0,

                "strategy": "Tidak ada data",

                "confidence": 0

            }



        goal = job.get(

            "goal",

            "unknown"

        )


        step = job.get(

            "step",

            "unknown"

        )



        score = 0

        status = "unknown"

        strategy = "Perlu analisis tambahan"

        confidence = 0.2



        # ==========================
        # SUCCESS EVALUATION
        # ==========================


        if job.get("status") == "completed":


            score = 100

            status = "success"

            strategy = (

                "Pertahankan metode"

            )

            confidence = 1.0




        elif job.get("success") is True:


            score = 90

            status = "success"


            strategy = (

                "Metode efektif, ulangi pola"

            )


            confidence = 0.9





        elif job.get("success") is False:


            score = 20

            status = "failed"


            strategy = (

                "Cari pendekatan alternatif"

            )


            confidence = 0.4




        result = {


            "goal":

            goal,


            "step":

            step,


            "score":

            score,


            "status":

            status,


            "strategy":

            strategy,


            "confidence":

            confidence,


            "time":

            datetime.now().isoformat()

        }





        # local history

        self.history.append(

            result

        )





        # permanent memory

        if self.memory:


            self.memory.remember(

                "adaptive_learning",

                result

            )



        return result






    # ==========================
    # HISTORY
    # ==========================


    def history_log(self):

        return self.history




    # ==========================
    # EXPERIENCE SUMMARY
    # ==========================


    def summary(self):


        total = len(

            self.history

        )


        if total == 0:


            return {


                "experience":0,

                "average_score":0

            }



        score = sum(

            x["score"]

            for x in self.history

        )



        return {


            "experience":

            total,


            "average_score":

            score / total

        }
