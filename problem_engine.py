class ProblemEngine:


    def analyze(self, device):

        problems=[]


        battery=device.get(
            "battery",
            100
        )


        temp=device.get(
            "temperature",
            0
        )


        storage=device.get(
            "storage",
            0
        )


        cpu=device.get(
            "cpu_load",
            0
        )


        if battery < 20:

            problems.append({

                "issue":
                "battery_low",

                "solution":
                "enable power saving"

            })


        if temp >= 45:

            problems.append({

                "issue":
                "device_hot",

                "solution":
                "reduce background activity"

            })


        if storage >= 90:

            problems.append({

                "issue":
                "storage_full",

                "solution":
                "cleanup cache"

            })


        if cpu >= 80:

            problems.append({

                "issue":
                "cpu_high",

                "solution":
                "stop heavy process"

            })


        return {

            "healthy":
            len(problems)==0,

            "problems":
            problems

        }
