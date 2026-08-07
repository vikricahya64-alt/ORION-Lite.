import asyncio
import signal

from worker import ORIONWorker
from orion_core import ORIONCore


class ORION:


    def __init__(self):

        self.worker = ORIONWorker()

        self.core = ORIONCore()

        self.running = True



    async def shutdown(self):

        print(
            "ORION SHUTDOWN SIGNAL RECEIVED"
        )

        self.running = False



    async def run(self):

        print(
            "ORION DAEMON STARTING"
        )


        while self.running:


            try:

                # 1. Jalankan pekerjaan yang sudah ada

                result = await self.worker.run_once()

                print(result)



                # 2. Jika queue kosong,
                # ORIONCore memutuskan apakah perlu membuat job

                if (
                    self.worker.queue.pending_count()
                    == 0
                ):

                    decision = self.core.heartbeat()


                    print(
                        "ORION CORE:",
                        decision
                    )



            except Exception as e:


                print(
                    "ORION ERROR:",
                    e
                )



            # hemat resource Android

            await asyncio.sleep(10)




async def main():


    agent = ORION()


    loop = asyncio.get_running_loop()


    for sig in (
        signal.SIGTERM,
        signal.SIGINT
    ):


        loop.add_signal_handler(

            sig,

            lambda:
            asyncio.create_task(
                agent.shutdown()
            )

        )


    await agent.run()



if __name__ == "__main__":

    asyncio.run(main())
