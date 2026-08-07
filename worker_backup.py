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

        # =========================
        # CORE SYSTEM
        # =========================

        self.queue = JobQueue()

        self.resource = ResourceManager()

        self.progress = ProgressTracker()

        self.memory = MemorySystem()

        self.supervisor = SupervisorAgent()


        # =========================
        # ANDROID ACTION
        # =========================

        self.action = AndroidAction()


        # =========================
        # AUTONOMOUS SYSTEM
        # =========================

        self.autonomous = AutonomousEngine()

        self.safety = SafetyPolicy()

        self.router = ActionRouter()



        # =========================
        # EVENT SYSTEM
        # =========================

        self.event_bus = EventBus()

        self.handlers = EventHandlers()


        self.event_bus.subscribe(
            "job_completed",
            self.handlers.job_completed
        )



        # =========================
        # AGENTS
        # =========================

        self.agents = {

            "learning":
            LearningAgent(),


            "task":
            TaskAgent(),


            "ai":
            AIAgent()

        }



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

        """
        ORION mengambil keputusan sendiri
        berdasarkan kondisi Android
        """

        try:


            device = self.resource.get_device()


            print(
                "REAL DEVICE:",
                device
            )


            decision = self.autonomous.decide(
                device
            )


            print(
                "ORION AUTONOMOUS DECISION:",
                decision
            )



            if decision["execute"]:


                permission = self.safety.allow(
                    decision
                )


                print(
                    "SAFETY POLICY:",
                    permission
                )



                if permission["allowed"]:


                    action_result = self.router.execute(
                        decision
                    )


                    print(
                        "AUTONOMOUS ACTION:",
                        action_result
                    )


                    self.memory.remember(

                        "autonomous_action",

                        {

                            "device":device,

                            "decision":decision,

                            "result":action_result

                        }

                    )


                else:


                    self.memory.remember(

                        "waiting_permission",

                        decision

                    )


        except Exception as e:


            print(
                "AUTONOMOUS ERROR:",
                str(e)
            )





    async def run_once(self):


        # =========================
        # 1. AUTONOMOUS BRAIN
        # =========================


        await self.autonomous_cycle()



        # =========================
        # 2. EXISTING JOB SYSTEM
        # =========================


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


            # =========================
            # AGENT EXECUTION
            # =========================


            agent_result = await self._call_agent(

                agent,

                job_data

            )



            # =========================
            # ANDROID ACTION EXISTING
            # =========================


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



            # =========================
            # SUPERVISOR
            # =========================


            evaluation = self.supervisor.evaluate(

                job_data,

                execution_result

            )



            # =========================
            # MEMORY
            # =========================


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



            error = {


                "executed":
                False,


                "error":
                str(e),


                "job":
                job_data

            }



            self.memory.remember(

                "error",

                error

            )



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
