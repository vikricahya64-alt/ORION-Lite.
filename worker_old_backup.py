import time
from datetime import datetime


from resource_manager import ResourceManager
from android_action import AndroidAction



class Worker:


    def __init__(
        self,
        queue=None,
        evaluator=None
    ):


        # =========================
        # Queue Compatibility
        # =========================

        self.queue = queue


        if self.queue is None:

            try:

                from job_queue import JobQueue

                self.queue = JobQueue()


            except Exception as e:

                print(
                    "QUEUE INIT ERROR:",
                    e
                )

                self.queue = None



        # =========================
        # Core Components
        # =========================

        self.resource = ResourceManager()

        self.action = AndroidAction()

        self.evaluator = evaluator



    # =========================
    # DEVICE READER
    # =========================

    def get_device(self):

        return self.resource.get_device()



    # =========================
    # EXECUTE JOB
    # =========================

    def execute_job(self, job):

        try:


            device = self.get_device()


            print(
                "REAL DEVICE:",
                device
            )


            data = job.get(
                "data",
                {}
            )


            data["device"] = device



            # Android Action

            action_result = self.action.execute(
                data
            )



            result = {

                "executed":
                    True,


                "device":
                    device,


                "action_result":
                    action_result,


                "time":
                    datetime.now().isoformat()

            }



            # Evaluation

            if self.evaluator:


                result["evaluation"] = (
                    self.evaluator.evaluate(
                        result
                    )
                )



            return result



        except Exception as e:


            raise e



    # =========================
    # PROCESS JOB
    # =========================

    def process(self, job):


        try:


            result = self.execute_job(job)



            if self.queue:


                self.queue.complete(
                    job,
                    result
                )



            return result



        except Exception as e:



            print(
                "WORKER ERROR:",
                e
            )



            if self.queue:


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
