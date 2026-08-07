import json
import os
from datetime import datetime


class JobQueue:

    def __init__(self):
        self.file = "jobs.json"

        if not os.path.exists(self.file):
            self.save([])

    def load(self):
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def save(self, jobs):
        with open(self.file, "w") as f:
            json.dump(jobs, f, indent=4)

    def add(self, job_type, data, priority=1):

        jobs = self.load()

        job = {
            "id": len(jobs) + 1,
            "type": job_type,
            "priority": priority,
            "status": "waiting",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "data": data
        }

        jobs.append(job)
        self.save(jobs)

        return {
            "status": "queued",
            "job": job
        }

    def next(self):

        jobs = self.load()

        waiting = [j for j in jobs if j["status"] == "waiting"]

        if not waiting:
            return None

        waiting.sort(key=lambda x: x["priority"])

        job_id = waiting[0]["id"]

        for job in jobs:

            if job["id"] == job_id:
                job["status"] = "running"
                job["updated_at"] = datetime.now().isoformat()
                self.save(jobs)
                return job

        return None

    def complete(self, job_id, result=None):

        jobs = self.load()

        for job in jobs:

            if job["id"] == job_id:

                job["status"] = "completed"
                job["completed_at"] = datetime.now().isoformat()
                job["result"] = result

                self.save(jobs)

                return {
                    "status": "completed",
                    "job": job
                }

        return {
            "status": "not_found"
        }

    def fail(self, job_id, error):

        jobs = self.load()

        for job in jobs:

            if job["id"] == job_id:

                job["status"] = "failed"
                job["failed_at"] = datetime.now().isoformat()
                job["error"] = str(error)

                self.save(jobs)

                return {
                    "status": "failed",
                    "job": job
                }

        return {
            "status": "not_found"
        }

    def pending_count(self):

        jobs = self.load()

        count = 0

        for job in jobs:

            if job["status"] in ("waiting", "running"):
                count += 1

        return count

    def cleanup_completed(self):

        jobs = self.load()

        active = []

        for job in jobs:

            if job["status"] not in ("completed", "failed"):
                active.append(job)

        self.save(active)
