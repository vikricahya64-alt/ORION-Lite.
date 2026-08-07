import subprocess
import json
import shutil


class ResourceManager:


    def __init__(self):

        self.state = {

            "temperature":30,

            "cpu_load":0

        }



    def get_device(self):

        """
        Membaca kondisi Android nyata
        melalui Termux API
        """

        device = {

            "battery":0,

            "charging":"UNKNOWN",

            "temperature":
                self.state["temperature"],

            "storage":0,

            "cpu_load":
                self.state["cpu_load"]

        }


        # Battery

        try:

            result = subprocess.run(
                [
                    "termux-battery-status"
                ],

                capture_output=True,

                text=True

            )


            data=json.loads(
                result.stdout
            )


            device["battery"] = data.get(
                "percentage",
                0
            )


            device["charging"] = data.get(
                "status",
                "UNKNOWN"
            )


        except Exception:

            pass



        # Storage

        try:

            usage = shutil.disk_usage("/")


            device["storage"] = round(
                (
                    (usage.used /
                    usage.total)
                    *100
                ),
                2
            )


        except Exception:

            pass



        return device



    def refresh(self):

        return self.get_device()



    def update_state(self,data):

        self.state.update(data)

        return self.state



    def can_execute(self,job):

        return True
