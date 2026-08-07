from datetime import datetime


class VerifyEngine:

    def verify(self, goal, device):
        """
        Entry point verifikasi.
        """

        if goal == "maintenance":
            return self.verify_maintenance(device)

        return {
            "allow": True,
            "risk": "low",
            "reason": "No verification rule",
            "time": datetime.now().isoformat()
        }

    def verify_maintenance(self, device):

        battery = device.get("battery", 100)
        charging = device.get("charging", "UNKNOWN")
        temperature = device.get("temperature", 0)
        storage = device.get("storage", 0)
        cpu = device.get("cpu_load", 0)

        # -----------------------
        # BATTERY
        # -----------------------

        if battery <= 15 and charging != "CHARGING":
            return {
                "allow": True,
                "risk": "medium",
                "reason": "Battery critical",
                "action": "battery_protection",
                "time": datetime.now().isoformat()
            }

        # -----------------------
        # TEMPERATURE
        # -----------------------

        if temperature >= 45:
            return {
                "allow": True,
                "risk": "high",
                "reason": "Temperature high",
                "action": "cooldown",
                "time": datetime.now().isoformat()
            }

        # -----------------------
        # STORAGE
        # -----------------------

        if storage >= 90:
            return {
                "allow": True,
                "risk": "medium",
                "reason": "Storage almost full",
                "action": "cleanup_cache",
                "time": datetime.now().isoformat()
            }

        # -----------------------
        # CPU
        # -----------------------

        if cpu >= 90:
            return {
                "allow": True,
                "risk": "medium",
                "reason": "CPU overload",
                "action": "reduce_workload",
                "time": datetime.now().isoformat()
            }

        # -----------------------
        # NORMAL
        # -----------------------

        return {
            "allow": True,
            "risk": "low",
            "reason": "Device healthy",
            "action": "health_check",
            "time": datetime.now().isoformat()
        }
