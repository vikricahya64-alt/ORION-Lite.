from datetime import datetime

from orion_worker_bridge import ORIONWorkerBridge


class WorkerBridgeAdapter:

    def __init__(self, old_worker=None):

        self.old_worker = old_worker

        self.bridge = ORIONWorkerBridge()

        self.running = True


    def run_once(self):

        try:

            autonomous_result = self.bridge.run_once()


            return {
                "status": "success",

                "source": "orion_worker_bridge",

                "time":
                    datetime.now().isoformat(),

                "autonomous":
                    autonomous_result
            }


        except Exception as e:


            return {

                "status": "error",

                "source":
                    "worker_bridge_adapter",

                "error":
                    str(e)

            }



    def execute_job(self, job):

        try:


            result = self.run_once()


            return {

                "job":
                    job,

                "execution":
                    result

            }


        except Exception as e:


            return {

                "job":
                    job,

                "error":
                    str(e)

            }



    def stop(self):

        self.running = False

        self.bridge.stop()
