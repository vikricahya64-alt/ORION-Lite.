from supervisor import SupervisorAgent
from worker import ORIONWorker
import asyncio
import time
import signal


class ORION:

    def __init__(self):
        self.supervisor = SupervisorAgent()
        self.worker = ORIONWorker()
        self.running = True


    def shutdown(self):
        print("ORION SHUTDOWN SIGNAL RECEIVED")
        self.running = False


    async def run(self):

        print("ORION DAEMON STARTING")

        # tunggu service Android/Termux siap
        time.sleep(5)

        print("ORION DAEMON ONLINE")


        while self.running:

            try:

                # buat rencana sistem
                plan = self.supervisor.execute(
                    "system_check"
                )


                print("\nPLAN:")
                print(plan)


                jobs = plan.get(
                    "total_jobs",
                    0
                )


                for _ in range(jobs):

                    if not self.running:
                        break


                    result = await self.worker.run_once()

                    print("\nRESULT:")
                    print(result)



            except Exception as e:

                print(
                    "ORION ERROR:",
                    e
                )


            # interval daemon
            await asyncio.sleep(60)



async def main():

    agent = ORION()


    # tangani shutdown service
    signal.signal(
        signal.SIGTERM,
        lambda s, f: agent.shutdown()
    )

    signal.signal(
        signal.SIGINT,
        lambda s, f: agent.shutdown()
    )


    await agent.run()



if __name__ == "__main__":

    try:

        asyncio.run(main())


    except KeyboardInterrupt:

        print(
            "ORION DAEMON STOPPED"
        )


    except Exception as e:

        print(
            "ORION FATAL ERROR:",
            e
        )
