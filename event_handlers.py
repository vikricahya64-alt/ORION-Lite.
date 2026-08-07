from memory_filter import MemoryFilter


class EventHandlers:

    def __init__(self):

        self.filter = MemoryFilter()


    async def job_completed(self, event):

        score = event["evaluation"]["score"]


        memory = {

            "event": "job_completed",

            "score": score,

            "data": event

        }


        result = self.filter.filter(memory)


        if result["save"]:

            print(
                "MEMORY SAVED"
            )

            return result


        print(
            "MEMORY DISCARDED"
        )

        return result
