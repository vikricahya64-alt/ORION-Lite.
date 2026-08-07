import subprocess
import json
import re
import os


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



    # ==========================
    # BATTERY REAL
    # ==========================

    def battery_info(self):


        data = self.run_cmd(
            "termux-battery-status"
        )


        if not data:

            return {

                "percentage":100,

                "status":"UNKNOWN",

                "temperature":0

            }



        try:

            return json.loads(data)


        except:

            return {}




    def battery(self):


        info = self.battery_info()


        return int(
            info.get(
                "percentage",
                100
            )
        )



    def charging(self):


        info = self.battery_info()


        return info.get(
            "status",
            "UNKNOWN"
        )



    def temperature(self):


        info = self.battery_info()


        try:

            return float(
                info.get(
                    "temperature",
                    0
                )
            )


        except:

            return 0





    # ==========================
    # STORAGE REAL
    # ==========================

    def storage(self):


        data = self.run_cmd(
            "df /data"
        )


        try:

            line = data.splitlines()[1]


            usage = line.split()[4]


            return int(
                usage.replace(
                    "%",
                    ""
                )
            )


        except:

            return 0






    # ==========================
    # CPU REAL %
    # ==========================

    def cpu_load(self):


        data = self.run_cmd(
            "top -n 1"
        )


        if not data:

            return 0



        try:

            idle = re.search(

                r'(\d+)%idle',

                data

            )


            if idle:


                idle_cpu = int(
                    idle.group(1)
                )


                cpu = (
                    100 -
                    idle_cpu
                )


                # Android multicore correction

                if cpu < 0:

                    cpu = 0


                if cpu >100:

                    cpu =100


                return cpu



        except:

            pass



        return 0





    # ==========================
    # MEMORY RAM
    # ==========================

    def memory(self):


        data = self.run_cmd(
            "free -m"
        )


        return data






    # ==========================
    # FINAL DEVICE STATE
    # ==========================

    def device_state(self):


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
            self.cpu_load(),


            "memory":
            self.memory()

        }




    # compatibility lama

    def status(self):

        return self.device_state()
