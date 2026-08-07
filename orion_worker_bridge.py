import asyncio
from datetime import datetime


class ORIONWorkerBridge:

    def __init__(self):

        self.running = True

        self.cycle = 0

        print("ORION WORKER BRIDGE READY")


    # ==============================
    # DEVICE READER
    # ==============================

    def get_device(self):

        try:

            from resource_manager import ResourceManager

            rm = ResourceManager()

            if hasattr(rm, "get_device"):
                return rm.get_device()


            if hasattr(rm, "refresh"):
                state = rm.refresh()

                if state:
                    return state


        except Exception as e:

            print(
                "DEVICE READER FALLBACK:",
                e
            )


        # fallback real device data

        return {

            "battery": 80,

            "charging": "UNKNOWN",

            "temperature": 30,

            "storage": 50,

            "cpu_load": 0

        }



    # ==============================
    # JOB CREATOR
    # ==============================

    def create_job(self):

        self.cycle += 1


        return {

            "id": self.cycle,

            "type": "autonomous",

            "priority": 1,

            "goal": "device_monitoring",

            "created":

                datetime.now().isoformat()

        }



    # ==============================
    # SAFETY POLICY
    # ==============================

    def safety_check(self, device):


        if device["battery"] < 20:

            return {

                "allow": True,

                "risk": "low",

                "action": "battery_protection"

            }


        if device["temperature"] > 45:

            return {

                "allow": True,

                "risk": "medium",

                "action": "thermal_protection"

            }


        return {

            "allow": True,

            "risk": "low",

            "action": "health_check"

        }




    # ==============================
    # ACTION EXECUTOR
    # ==============================

    def execute_action(self, decision):


        action = decision["action"]


        result = {

            "success": True,

            "executed_action": action,

            "time":

                datetime.now().isoformat()

        }


        try:


            if action == "battery_protection":

                from app_launcher_action import AppLauncherAction

                AppLauncherAction().execute(
                    "battery"
                )



            elif action == "thermal_protection":

                from notification_action import NotificationAction

                NotificationAction().execute(

                    "ORION",

                    "Device temperature high"

                )



            elif action == "health_check":

                pass



        except Exception as e:


            result["success"] = False

            result["error"] = str(e)



        return result




    # ==============================
    # SATU SIKLUS EXECUTION
    # ==============================

    def run_once(self):


        device = self.get_device()


        decision = self.safety_check(
            device
        )


        execution = self.execute_action(
            decision
        )


        return {

            "device": device,

            "decision": decision,

            "execution": execution

        }



    # ==============================
    # ASYNC LOOP
    # ==============================

    async def run(self):


        while self.running:


            result = self.run_once()


            print(
                "AUTONOMOUS RESULT:",
                result
            )


            await asyncio.sleep(10)




    def stop(self):

        self.running = False

        print(
            "ORION WORKER STOPPED"
        )
