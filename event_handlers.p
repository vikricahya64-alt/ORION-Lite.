from datetime import datetime

from memory_filter import MemoryFilter
from memory import Memory


class EventHandlers:


    def __init__(self):

        self.memory_filter = MemoryFilter()
        self.memory = Memory()



    async def job_completed(self, event):


        job = event.get(
            "job",
            {}
        )


        result = event.get(
            "result",
            {}
        )


        score = 0


        if result.get("executed"):

            score = 100

        else:

            score = 20



        memory_record = {

            "category": "job_completed",

            "score": score,

            "decision":
                "success"
                if score >= 70
                else "retry",

            "job": job,

            "time":
                datetime.now().isoformat()

        }


        filtered = self.memory_filter.filter(
            memory_record
        )


        if filtered["save"]:


            saved = self.memory.save(
                filtered["memory"]
            )


            return {

                "event":
                    "job_completed",

                "memory":
                    "saved",

                "data":
                    saved

            }


        return {

            "event":
                "job_completed",

            "memory":
                "discarded",

            "reason":
                filtered["reason"]

        }
