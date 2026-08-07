import subprocess
import json


class AndroidMonitor:

    def run_cmd(self, cmd):

        try:
            result = subprocess.check_output(
                cmd,
                shell=True
            )

            return result.decode()

        except:
            return None


    def battery(self):

        data = self.run_cmd(
            "termux-battery-status"
        )

        if data:
            return json.loads(data)

        return {}


    def storage(self):

        data = self.run_cmd(
            "df /data"
        )

        return data


    def temperature(self):

        battery = self.battery()

        return battery.get(
            "temperature",
            0
        )


    def get_state(self):

        battery = self.battery()

        return {

            "battery":
                battery.get(
                    "percentage",
                    0
                ),

            "charging":
                battery.get(
                    "status",
                    ""
                ),

            "temperature":
                self.temperature(),

            "storage":
                self.storage()

        }
