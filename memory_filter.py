class MemoryFilter:


    def __init__(self):

        self.minimum_score = 70



    def should_save(self, memory):

        score = memory.get(
            "score",
            0
        )


        decision = memory.get(
            "decision",
            ""
        )


        if score >= self.minimum_score:

            return True


        if decision in (
            "important",
            "learn",
            "success"
        ):

            return True


        return False



    def filter(self, memory):

        if self.should_save(memory):

            return {

                "save": True,

                "memory": memory

            }


        return {

            "save": False,

            "reason": "Low value memory"

        }
