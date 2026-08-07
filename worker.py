import asyncio
from datetime import datetime

from worker_bridge_adapter import WorkerBridgeAdapter


class Worker:


    def __init__(self, queue=None):

        self.queue = queue

        self.running = True

        self.bridge = WorkerBridgeAdapter(self)


        print(
            "ORION WORKER INITIALIZED"
        )



    # ==========================
    # Job lama ORION
    # ==========================

    def get_job(self):

        try:

            if self.queue is None:

                return None


            if hasattr(self.queue, "get_next"):

                return self.queue.get_next()


            if hasattr(self.queue, "get"):

                return self.queue.get()


        except Exception as e:

            print(
                "JOB READ ERROR:",
                e
            )


        return None



    # ==========================
    # Autonomous Bridge
    # ==========================

    def autonomous_cycle(self):

        try:

            result = self.bridge.run_once()


            print(
                "ORION AUTONOMOUS:",
                result
            )


            return result


        except Exception as e:


            print(
                "AUTONOMOUS ERROR:",
                e
            )


            return {

                "status":"error",

                "error":str(e)

            }



    # ==========================
    # Execute Job
    # ==========================

    def execute(self, job):

        try:


            autonomous = self.autonomous_cycle()


            return {

                "executed": True,

                "job": job,

                "autonomous":

                    autonomous,

                "time":

                    datetime.now().isoformat()

            }


        except Exception as e:


            return {

                "executed":False,

                "error":str(e)

            }




    # ==========================
    # Single Worker Cycle
    # ==========================

    async def run_once(self):


        job = self.get_job()


        if job is None:

            return {

                "status":"idle",

                "message":
                    "No job available"

            }



        result = self.execute(job)



        return {

            "status":"completed",

            "result":result

        }



    # ==========================
    # Worker Loop
    # ==========================

    async def run(self):


        while self.running:


            try:


                result = await self.run_once()


                print(
                    "WORKER RESULT:",
                    result
                )


            except Exception as e:


                print(
                    "WORKER LOOP ERROR:",
                    e
                )



            await asyncio.sleep(10)




    def stop(self):

        self.running = False


        self.bridge.stop()


        print(
            "WORKER STOPPED"
        )
