from job_queue import JobQueue


class Dispatcher:

    def __init__(self):

        self.queue = JobQueue()


    def dispatch(self, decision, plan):

        action = decision["action"]


        if action == "task":

            return self.queue.add(
                "task",
                plan,
                priority=5
            )


        if action == "learning":

            return self.queue.add(
                "learning",
                plan,
                priority=4
            )


        return self.queue.add(
            "ai",
            plan,
            priority=2
        )
