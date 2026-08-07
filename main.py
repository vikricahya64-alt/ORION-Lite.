import asyncio
import signal


from orion_worker_bridge import ORIONWorkerBridge
from orion_core import ORIONCore

from orion_kernel import ORIONKernel
from agents.supervisor_agent import SupervisorAgent

from memory import MemorySystem
from adaptive_learning import AdaptiveLearning



class ORION:


    def __init__(self):


        # ==========================
        # Kernel
        # ==========================

        self.kernel = ORIONKernel()

        self.kernel.boot()



        # ==========================
        # Memory System
        # ==========================

        self.memory = MemorySystem()



        # ==========================
        # Adaptive Learning
        # ==========================

        self.adaptive = AdaptiveLearning(

            self.memory

        )



        # ==========================
        # Supervisor Agent
        # ==========================

        self.supervisor = SupervisorAgent(

            self.kernel,

            self.memory,

            self.adaptive

        )


        self.kernel.register(

            "supervisor",

            self.supervisor

        )



        # ==========================
        # Worker
        # ==========================

        self.worker = ORIONWorkerBridge()



        # ==========================
        # Core
        # ==========================

        self.core = ORIONCore()



        self.running = True





    async def shutdown(self):


        print(

            "ORION SHUTDOWN SIGNAL RECEIVED"

        )


        self.running = False


        self.kernel.shutdown()






    async def run(self):


        print(

            "ORION DAEMON STARTING"

        )



        while self.running:


            try:


                # ==========================
                # Kernel heartbeat
                # ==========================


                kernel_state = (

                    self.kernel.heartbeat()

                )


                print(

                    "KERNEL:",

                    kernel_state

                )




                # ==========================
                # Supervisor
                # ==========================


                supervisor_state = (

                    self.supervisor.run_once()

                )


                print(

                    "SUPERVISOR:",

                    supervisor_state

                )





                # ==========================
                # Worker Execution
                # ==========================


                worker_result = (

                    self.worker.run_once()

                )


                print(

                    "WORKER:",

                    worker_result

                )





                # ==========================
                # Adaptive Learning
                # ==========================


                execution = worker_result.get(

                    "execution",

                    {}

                )



                learning_job = {


                    "goal":

                    "worker_execution",



                    "step":

                    worker_result.get(

                        "decision",

                        {}

                    ).get(

                        "action",

                        "unknown"

                    ),



                    "success":

                    execution.get(

                        "success",

                        False

                    )

                }




                learning_result = (

                    self.adaptive.analyze(

                        learning_job

                    )

                )



                print(

                    "ADAPTIVE LEARNING:",

                    learning_result

                )






                # ==========================
                # ORION Core Decision
                # ==========================


                if self.core.queue.pending_count() == 0:


                    decision = (

                        self.core.heartbeat()

                    )


                    print(

                        "ORION CORE:",

                        decision

                    )





            except Exception as e:


                print(

                    "ORION ERROR:",

                    e

                )





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
