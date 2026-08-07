from datetime import datetime


class SafetyPolicy:


    def __init__(self):

        self.user_priority = True

        self.allow_autonomous = True



    def evaluate(self, device, goal):


        battery = device.get(
            "battery",
            100
        )

        temperature = device.get(
            "temperature",
            30
        )

        storage = device.get(
            "storage",
            0
        )

        cpu = device.get(
            "cpu_load",
            0
        )


        decision = {

            "allow": True,

            "risk": "low",

            "action": "health_check",

            "reason": "normal",

            "time":
                datetime.now().isoformat()

        }



        # =====================
        # USER PRIORITY
        # =====================

        if self.user_priority:

            decision["reason"] = (
                "User priority protection active"
            )



        # =====================
        # BATTERY POLICY
        # =====================

        if battery <= 20:


            decision.update({

                "action":
                    "battery_protection",

                "risk":
                    "medium",

                "reason":
                    "Battery below limit"

            })



        # =====================
        # THERMAL POLICY
        # =====================

        if temperature >= 45:


            decision.update({

                "action":
                    "thermal_protection",

                "risk":
                    "high",

                "reason":
                    "Device temperature high"

            })



        # =====================
        # STORAGE POLICY
        # =====================

        if storage >= 90:


            decision.update({

                "action":
                    "storage_cleanup",

                "risk":
                    "medium",

                "reason":
                    "Storage critical"

            })



        # =====================
        # CPU POLICY
        # =====================

        if cpu >= 90:


            decision.update({

                "action":
                    "reduce_activity",

                "risk":
                    "medium",

                "reason":
                    "CPU overloaded"

            })



        return decision
