from memory import MemorySystem



class DecisionMemory:


    def __init__(self):

        self.memory = MemorySystem()

        self.category = "decision"



    def record(self, goal, decision):


        return self.memory.remember(

            self.category,

            {

                "goal": goal,

                "decision": decision

            }

        )



    def history(self):


        return self.memory.recall(

            self.category

        )



    def success_rate(self, goal):


        records = self.history()


        matches = [

            r for r in records

            if r["data"]["goal"] == goal

        ]


        if not matches:

            return 0



        success = 0


        for item in matches:

            decision = item["data"]["decision"]


            if decision.get("confidence", 0) >= 0.8:

                success += 1



        return success / len(matches)
