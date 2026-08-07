import subprocess
import json
import shutil


class DeviceProvider:


    def run_command(self, command):

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            return result.stdout.strip()

        except Exception:

            return None



    def battery(self):

        try:

            data = self.run_command(
                [
                    "termux-battery-status"
                ]
            )

            info = json.loads(data)

            return {
                "battery": info.get(
                    "percentage",
                    0
                ),

                "charging": info.get(
                    "status",
                    "UNKNOWN"
                )
            }

        except Exception:

            return {
                "battery":0,
                "charging":"UNKNOWN"
            }



    def storage(self):

        try:

            result = shutil.disk_usage(
                "/data/data/com.termux"
            )

            total = result.total
            free = result.free

            used = (
                (total-free)
                /
                total
            )*100


            return round(
                used,
                2
            )

        except Exception:

            return 0



    def temperature(self):

        return 30



    def cpu(self):

        return 0



    def get_device(self):

        battery = self.battery()


        return {

            "battery":
                battery["battery"],

            "charging":
                battery["charging"],

            "temperature":
                self.temperature(),

            "storage":
                self.storage(),

            "cpu_load":
                self.cpu()

        }
