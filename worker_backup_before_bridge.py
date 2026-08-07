

                try:

                    self.queue.fail(
                        job,
                        str(e)
                    )


                except Exception as queue_error:


                    print(
                        "JOBQUEUE ERROR:",
                        queue_error
                    )



            return {

                "executed":
                    False,

                "error":
                    str(e)

            }



    # =========================
    # SINGLE LOOP
    # =========================

    def run_once(self):


        if self.queue is None:


            return {

                "status":
                    "idle",

                "message":
                    "Queue unavailable"

            }



        try:


            job = self.queue.get_next()



            if not job:


                return {

                    "status":
                        "idle",

                    "message":
                        "No job available"

                }



            return self.process(job)



        except Exception as e:


            print(
                "WORKER LOOP ERROR:",
                e
            )


            return {

                "status":
                    "error",

                "error":
                    str(e)

            }



    # =========================
    # CONTINUOUS LOOP
    # =========================

    def run_forever(
        self,
        interval=10
    ):


        while True:


            result = self.run_once()


            print(
                result
            )


            time.sleep(
                interval
            )





# =================================================
# ORION COMPATIBILITY ALIAS
# main.py menggunakan nama ini
# =================================================

ORIONWorker = Worker
