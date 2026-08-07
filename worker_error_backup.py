import time
from datetime import datetime


from resource_manager import ResourceManager
from android_action import AndroidAction



class Worker:


    def __init__(
        self,
        queue,
        evaluator=None
    ):


        self.queue = queue

        self.resource = ResourceManager()

        self.action = AndroidAction()

        self.evaluator = evaluator



    # =========================
    # GET DEVICE
    # =========================

    def get_device(self):

        return self.resource.get_device()



    # =========================
    # PROCESS JOB
    # =========================

    def process(self, job):


        try:


            device = self.get_device()



            data = job.get(
                "data",
                {}
            )


            data["device"] = device



            print(
                "REAL DEVICE:",
                device
            )



            # =====================
            # ACTION EXECUTION
            # =====================

            result = self.action.execute(
                data
            )



            execution = {

                "executed":
                    True,

                "result":
                    result

            }



            # =====================
            # EVALUATION
            # =====================

            evaluation = None


            if self.evaluator:


                evaluation = self.evaluator.evaluate(
                    execution
                )



            response = {

                "execution":
                    execution,


                "evaluation":
                    evaluation,


                "time":
                    datetime.now().isoformat()

            }



            # COMPLETE JOB

            self.queue.complete(
                job,
                response
            )


            return response



        except Exception as e:


            print(
                "WORKER ERROR:",
                e
            )


            # =====================
            # SAFE FAIL HANDLING
            # =====================

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
    # LOOP
    # =========================

    def run_once(self):

        try:

            job = self.queue.get_next()

            if not job:

                return {
                    "status": "idle",
                    "message": "No job available"
                }

            return self.process(job)


        except Exception as e:

            print(
                "WORKER LOOP ERROR:",
                e
            )

            return {
                "status":"error",
                "error":str(e)
            }



# Compatibility untuk main.py ORION

ORIONWorker = Worker
