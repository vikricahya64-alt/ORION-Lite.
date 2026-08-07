import inspect

from event_bus import EventBus
from event_handlers import EventHandlers
from job_queue import JobQueue
from resource_manager import ResourceManager
from progress_tracker import ProgressTracker
from memory import MemorySystem
from supervisor import SupervisorAgent

from android_action import AndroidAction

from autonomous_engine import AutonomousEngine
from safety_policy import SafetyPolicy
from action_router import ActionRouter


from agents.learning import LearningAgent
from agents.task import TaskAgent
from agents.ai import AIAgent



class ORIONWorker:


    def __init__(self):

        self.queue = JobQueue()

        self.resource = ResourceManager()

        self.progress = ProgressTracker()

        self.memory = MemorySystem()

        self.supervisor = SupervisorAgent()


        # Android executor lama
        self.action = AndroidAction()


        # Autonomous system baru
        self.autonomous = AutonomousEngine()

        self.safety = SafetyPolicy()

        self.router = ActionRouter()



        self.event_bus = EventBus()

        self.handlers = EventHandlers()


        self.event_bus.subscribe(
            "job_completed",
            self.handlers.job_completed
        )



        self.agents = {

            "learning":
            LearningAgent(),

            "task":
            TaskAgent(),

            "ai":
            AIAgent()

        }




    # ==================================
    # RESOURCE MANAGER ADAPTER
    # ==================================

    def get_device_state(self):

        """
        Membaca kondisi Android
        kompatibel dengan ResourceManager lama
        """

        if hasattr(
            self.resource,
            "get_device"
        ):

            return self.resource.get_device()



        elif hasattr(
            self.resource,
            "read"
        ):

            return self.resource.read()



        elif hasattr(
            self.resource,
            "collect"
        ):

            return self.resource.collect()



        elif hasattr(
            self.resource,
            "status"
        ):

            return self.resource.status()



        elif hasattr(
            self.resource,
            "get_status"
        ):

            return self.resource.get_status()



        else:

            raise Exception(
                "ResourceManager tidak memiliki fungsi device reader"
            )






    async def _call_agent(
        self,
        agent,
        job_data
    ):


        if hasattr(agent,"run"):

            fn = agent.run


        elif hasattr(agent,"learn"):

            fn = agent.learn


        elif hasattr(agent,"execute"):

            fn = agent.execute


        else:

            raise Exception(
                "Agent method tidak ditemukan"
            )



        if inspect.iscoroutinefunction(fn):

            return await fn(job_data)



        result = fn(job_data)



        if inspect.isawaitable(result):

            return await result



        return result






    async def autonomous_cycle(self):


        try:


            # =============================
            # BACA DEVICE NYATA
            # =============================

            device = self.get_device_state()



            print(
                "AUTONOMOUS DEVICE:",
                device
            )



            # =============================
            # BUAT KEPUTUSAN
            # =============================

            decision = self.autonomous.decide(
                device
            )



            print(
                "ORION AUTONOMOUS DECISION:",
                decision
            )



            # =============================
            # EKSEKUSI JIKA DIPERLUKAN
            # =============================

            if decision["execute"]:


                permission = self.safety.allow(
                    decision
                )


                print(
                    "SAFETY POLICY:",
                    permission
                )



                if permission["allowed"]:


                    result = self.router.execute(
                        decision
                    )


                    print(
                        "AUTONOMOUS ACTION:",
                        result
                    )


                    self.memory.remember(

                        "autonomous_action",

                        {

                            "device":
                            device,

                            "decision":
                            decision,

                            "result":
                            result

                        }

                    )


                else:


                    print(
                        "ACTION WAIT USER APPROVAL"
                    )


                    self.memory.remember(

                        "approval_required",

                        decision

                    )



        except Exception as e:


            print(
                "AUTONOMOUS ERROR:",
                e
            )








    async def run_once(self):


        # =================================
        # AUTONOMOUS ENGINE
        # =================================

        await self.autonomous_cycle()



        # =================================
        # QUEUE SYSTEM LAMA
        # =================================


        job = self.queue.next()



        if job is None:


            return {

                "status":
                "idle",

                "message":
                "No job available"

            }



        job_data = job.get(
            "data",
            {}
        )



        job_type = job.get(
            "type",
            "task"
        )



        agent = self.agents.get(

            job_type,

            self.agents["task"]

        )



        try:



            agent_result = await self._call_agent(

                agent,

                job_data

            )



            action_result = self.action.execute(

                job_data

            )



            execution_result = {


                "executed":
                True,


                "agent_result":
                agent_result,


                "action_result":
                action_result,


                "data":
                job_data

            }



            evaluation = self.supervisor.evaluate(

                job_data,

                execution_result

            )



            self.memory.remember(

                "execution",

                {

                    "job":
                    job_data,


                    "result":
                    execution_result,


                    "evaluation":
                    evaluation

                }

            )



            self.queue.complete(

                job["id"]

            )



            return {


                "status":
                "completed",


                "job":
                job,


                "execution":
                execution_result,


                "evaluation":
                evaluation

            }



        except Exception as e:



            if hasattr(
                self.queue,
                "fail"
            ):

                self.queue.fail(
                    job["id"]
                )


            return {

                "status":
                "failed",

                "error":
                str(e)

            }
