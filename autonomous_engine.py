from datetime import datetime


class AutonomousEngine:


    def decide(self, device):

        battery = device.get("battery",100)
        temperature = device.get("temperature",0)
        storage = device.get("storage",0)
        cpu = device.get("cpu_load",0)



        # Battery

        if battery <= 20:

            return {
                "execute": True,
                "action": "battery",
                "risk": "medium",
                "reason": "Battery low",
                "approval": False
            }



        # Temperature

        if temperature >=45:

            return {
                "execute": True,
                "action": "temperature",
                "risk":"high",
                "reason":"Device hot",
                "approval":True
            }



        # Storage

        if storage >=90:

            return {
                "execute": True,
                "action":"storage",
                "risk":"medium",
                "reason":"Storage full",
                "approval":True
            }



        # CPU

        if cpu >=90:

            return {
                "execute":True,
                "action":"performance",
                "risk":"low",
                "reason":"CPU overload",
                "approval":False
            }



        return {

            "execute":False,
            "action":"none",
            "risk":"low",
            "reason":"Normal",
            "approval":False,
            "time":datetime.now().isoformat()

        }
