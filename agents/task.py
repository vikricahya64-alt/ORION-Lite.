class TaskAgent:


    async def execute(self, data):

        return {

            "executed": True,

            "type": "task",

            "data": data

        }
