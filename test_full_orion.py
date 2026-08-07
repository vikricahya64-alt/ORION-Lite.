import asyncio

from supervisor import SupervisorAgent
from worker import ORIONWorker


async def main():

    print("=== ORION FULL TEST ===")


    supervisor = SupervisorAgent()

    worker = ORIONWorker()


    result = supervisor.execute(

        "Belajar membuat AI Agent"

    )


    print("\nSUPERVISOR:")

    print(result)


    print("\nWORKER:")


    for i in range(
        result["total_jobs"]
    ):

        output = await worker.run_once()

        print(output)



asyncio.run(main())
