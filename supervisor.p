from decision_engine import DecisionEngine
from planner import PlannerAgent
from job_queue import JobQueue


class SupervisorAgent:

    def __init__(self):

        self.decision = DecisionEngine()

        self.planner = PlannerAgent()

        self.queue = JobQueue()


    def analyze(self, goal):

        decision = self.decision.decide(goal)

        plan = self.planner.create_plan(goal)


        plan["action"] = decision["action"]

        plan["priority"] = decision["priority"]


        return {

            "decision": decision,

            "plan": plan

        }


    def execute(self, goal):

        analysis = self.analyze(goal)

        plan = analysis["plan"]

        jobs = []


        for step in plan["steps"]:

            job = self.queue.add(

                plan["action"],

                {

                    "goal": goal,

                    "step": step,

                    "priority": plan["priority"]

                },

                priority=plan["priority"]

            )

            jobs.append(job)


        return {

            "status": "planned",

            "goal": goal,

            "action": plan["action"],

            "priority": plan["priority"],

            "total_jobs": len(jobs),

            "jobs": jobs

        }
