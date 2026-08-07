from datetime import datetime


class WorkerRuntime:

    def __init__(self, bridge=None, queue=None):

        self.bridge = bridge
        self.queue = queue

        print("ORION WORKER RUNTIME READY")


    def execute_job(self, job):

        try:

            if self.bridge:

                result = self.bridge.run_once()

                return {
                    "success": True,
                    "source": "worker_runtime",
                    "job": job,
                    "result": result,
                    "time": datetime.now().isoformat()
                }


            return {
                "success": False,
                "error": "Bridge not connected"
            }


        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }



    def autonomous_cycle(self):

        try:

            if self.bridge:

                return {
                    "success": True,
                    "source": "worker_runtime",
                    "autonomous":
                        self.bridge.run_once(),
                    "time":
                        datetime.now().isoformat()
                }


            return {
                "success": False,
                "error": "No bridge"
            }


        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }
