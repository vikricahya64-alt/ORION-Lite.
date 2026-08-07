from apscheduler.schedulers.background import BackgroundScheduler


class SchedulerEngine:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def get_jobs(self):
        return self.scheduler.get_jobs()

    def add_job(self, *args, **kwargs):
        return self.scheduler.add_job(*args, **kwargs)

    def remove_job(self, job_id):
        return self.scheduler.remove_job(job_id)

    def shutdown(self):
        self.scheduler.shutdown(wait=False)

    def should_run(self, job, system_state):
        job_type = job.get("type", "")
        mode = system_state.get("mode", "normal")
        battery = system_state.get("battery", 100)

        if mode == "save_energy" and job_type == "learning":
            return {
                "run": False,
                "reason": "Learning ditunda karena hemat energi"
            }

        if battery < 20 and job_type == "learning":
            return {
                "run": False,
                "reason": "Baterai rendah"
            }

        return {
            "run": True,
            "reason": "Kondisi mendukung"
        }
