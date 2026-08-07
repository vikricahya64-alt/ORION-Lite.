from datetime import datetime, timedelta


class RuntimeController:

    def __init__(self):

        # waktu terakhir ORION berjalan
        self.last_run = None

        # status runtime
        self.running = True

        # batas interval cycle
        self.interval_seconds = 10


    def can_run(self):

        if not self.running:
            return False


        now = datetime.now()


        # pertama kali jalan
        if self.last_run is None:
            self.last_run = now
            return True


        elapsed = (
            now - self.last_run
        ).total_seconds()


        if elapsed >= self.interval_seconds:

            self.last_run = now
            return True


        return False



    def sleep(self):

        self.running = False



    def wake(self):

        self.running = True



    def status(self):

        return {

            "running": self.running,

            "last_run":
                self.last_run.isoformat()
                if self.last_run
                else None,

            "interval_seconds":
                self.interval_seconds

        }
