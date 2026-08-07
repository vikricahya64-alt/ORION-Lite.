from job_queue import JobQueue
from adaptive_controller import AdaptiveController
from runtime_controller import RuntimeController
from problem_engine import ProblemEngine
from device_monitor import DeviceMonitor

from datetime import datetime
import time


class ORIONCore:


    def __init__(self):

        self.queue = JobQueue()

        self.adaptive = AdaptiveController()

        self.runtime = RuntimeController()

        self.problem = ProblemEngine()

        self.device = DeviceMonitor()

        self.counter = 0

        self.last_state = None

        self.last_action_time = None

        self.cooldown_seconds = 300



    def get_device_state(self):

        return self.device.status()



    def heartbeat(self):


        try:


            # =========================
            # Runtime protection
            # =========================

            if not self.runtime.can_run():

                return {

                    "status":
                    "sleep",

                    "message":
                    "waiting next cycle"

                }



            # =========================
            # Queue protection
            # =========================

            if self.queue.pending_count() > 0:


                return {

                    "status":
                    "queue_busy"

                }



            # =========================
            # Read Android device
            # =========================

            device = self.get_device_state()


            print(
                "REAL DEVICE:",
                device
            )



            # =========================
            # Problem analysis
            # =========================

            analysis = self.problem.analyze(
                device
            )


            print(
                "ORION ANALYSIS:",
                analysis
            )



            # =========================
            # Adaptive decision
            # =========================

            decision = self.adaptive.evaluate(
                device
            )


            print(
                "ORION DECISION:",
                decision
            )



            # =========================
            # Emergency mode
            # =========================

            if not decision["allow"]:


                job = self.queue.add(

                    job_type="task",

                    priority=0,


                    data={

                        "goal":
                        "emergency",


                        "step":
                        decision["reason"],


                        "device":
                        device,


                        "source":
                        "orion_core",


                        "created":
                        datetime.now().isoformat()

                    }

                )


                return {

                    "status":
                    "emergency",

                    "job":
                    job

                }




            # =========================
            # Stable check
            # =========================

            if self.last_state == device:


                if self.last_action_time:


                    elapsed = (

                        datetime.now()

                        -

                        self.last_action_time

                    ).seconds



                    if elapsed < self.cooldown_seconds:


                        return {


                            "status":
                            "stable",


                            "message":
                            "Waiting next evaluation",


                            "next_check":
                            self.cooldown_seconds - elapsed

                        }




            # =========================
            # Create new task
            # =========================

            self.counter += 1



            if analysis["healthy"]:


                goal = "maintenance"


                step = (

                    "device monitoring cycle "

                    + str(self.counter)

                )


            else:


                problem = analysis["problems"][0]


                goal = "repair"


                step = (

                    problem["issue"]

                    +

                    " -> "

                    +

                    problem["solution"]

                )




            job = self.queue.add(

                job_type="task",

                priority=1,


                data={


                    "goal":
                    goal,


                    "step":
                    step,


                    "device":
                    device,


                    "source":
                    "orion_core",


                    "created":
                    datetime.now().isoformat()


                }

            )



            print(
                "ORION CREATED JOB:",
                job
            )



            # simpan state

            self.last_state = device


            self.last_action_time = datetime.now()



            return job




        except Exception as e:


            print(
                "ORION CORE ERROR:",
                e
            )


            return {


                "status":
                "error",


                "message":
                str(e)

            }
