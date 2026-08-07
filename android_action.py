import os
from datetime import datetime

from safety_policy import SafetyPolicy

from action_executor import ActionExecutor



class AndroidAction:


    def __init__(self):

        self.policy = SafetyPolicy()

        self.executor = ActionExecutor()



    def execute(self, data):


        device = data.get(
            "device",
            {}
        )


        goal = data.get(
            "goal",
            ""
        )



        # =========================
        # SAFETY POLICY DECISION
        # =========================

        decision = self.policy.evaluate(
            device,
            goal
        )



        if not decision.get(
            "allow",
            False
        ):

            return {

                "time":
                    datetime.now().isoformat(),

                "decision":
                    decision,

                "execution":
                {

                    "success":
                        False,

                    "message":
                        "Blocked by safety policy"

                }

            }



        # =========================
        # EXECUTION
        # =========================


        action_name = decision.get(
            "action",
            "health_check"
        )



        execution = self.executor.execute(
            action_name,
            data
        )



        # =========================
        # RESULT
        # =========================


        return {


            "time":
                datetime.now().isoformat(),


            "goal":
                goal,


            "decision":
                decision,


            "execution":
                execution


        }
