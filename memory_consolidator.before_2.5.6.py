from memory import MemorySystem


class MemoryConsolidator:


    def __init__(self):

        self.memory = MemorySystem()



    def process(self, event):

        job = event.get(
            "job",
            {}
        )


        goal = job.get(
            "goal",
            "unknown"
        )


        step = job.get(
            "step",
            ""
        )


        existing = self.memory.recall()


        for item in existing:

            data = item.get(
                "data",
                {}
            )

            if (
                data.get("goal") == goal
                and
                data.get("step") == step
            ):

                return {

                    "status": "duplicate",

                    "goal": goal,

                    "step": step

                }



        saved = self.memory.remember(

            "experience",

            {

                "goal": goal,

                "step": step,

                "status": "completed"

            }

        )


        return {

            "status": "stored",

            "memory": saved

        }
