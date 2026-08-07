import time


class SleepManager:


    def __init__(self):

        self.sleeping = False

        self.last_activity = time.time()



    def activity(self):

        self.last_activity = time.time()

        self.sleeping = False



    def should_sleep(
        self,
        worker_status,
        idle_time=300
    ):

        now = time.time()

        inactive = now - self.last_activity


        if worker_status == "idle" and inactive >= idle_time:

            return True


        return False



    def sleep(self):

        self.sleeping = True

        return {

            "mode": "sleep",

            "message": "ORION masuk mode hemat energi"

        }



    def wake(self):

        self.sleeping = False

        self.activity()

        return {

            "mode": "active",

            "message": "ORION aktif kembali"

        }
