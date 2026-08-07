from device_monitor import DeviceMonitor


class HealthMonitor:

    def __init__(self):

        self.device = DeviceMonitor()


    def check(self):

        device_state = self.device.status()

        battery = device_state["battery"]

        percentage = battery.get(
            "percentage",
            0
        )

        temperature = battery.get(
            "temperature",
            0
        )


        if percentage < 20:

            mode = "save_energy"

        elif temperature > 40:

            mode = "cooldown"

        else:

            mode = "normal"


        return {

            "system": "ORION-Lite",

            "status": "healthy",

            "mode": mode,

            "battery": percentage,

            "temperature": temperature

        }
