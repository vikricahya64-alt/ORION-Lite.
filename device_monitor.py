import subprocess
import json
import re


class DeviceMonitor:


    def run_cmd(self, cmd):

        try:

            result = subprocess.check_output(
                cmd,
                shell=True,
                stderr=subprocess.DEVNULL
            )

            return result.decode().strip()


        except Exception:

            return ""



    def battery(self):

        data = self.run_cmd(
            "termux-battery-status"
        )


        try:

            info = json.loads(data)

            return int(
                info.get(
                    "percentage",
                    100
                )
            )


        except:

            return 100





    def charging(self):

        data = self.run_cmd(
            "termux-battery-status"
        )


        try:

            info = json.loads(data)

            status = info.get(
                "status",
                "UNKNOWN"
            )


            if status:

                return status


        except:

            pass


        return "UNKNOWN"





    def temperature(self):

        data = self.run_cmd(
            "termux-battery-status"
        )


        try:

            info = json.loads(data)

            return float(
                info.get(
                    "temperature",
                    0
                )
            )


        except:

            return 0





    def storage(self):

        data = self.run_cmd(
            "df /data"
        )


        try:

            lines = data.splitlines()


            if len(lines) > 1:

                usage = lines[1].split()[4]

                return int(
                    usage.replace(
                        "%",
                        ""
                    )
                )


        except:

            pass


        return 0





    def cpu_load(self):

        data = self.run_cmd(
            "cat /proc/loadavg"
        )


        try:

            load = float(
                data.split()[0]
            )


            # normalisasi Android
            if load < 0:

                load = 0


            return load


        except:

            return 0





    def status(self):

        return {


            "battery":
            self.battery(),



            "charging":
            self.charging(),



            "temperature":
            self.temperature(),



            "storage":
            self.storage(),



            "cpu_load":
            self.cpu_load()

        }
