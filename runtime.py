import asyncio

import config

from worker import ORIONWorker
from health_monitor import HealthMonitor
from sleep_manager import SleepManager
from optimizer import DatabaseOptimizer
from memory_cleaner import MemoryCleaner


class ORIONRuntime:

    def __init__(self):

        self.worker = ORIONWorker()

        self.health = HealthMonitor()

        self.sleep = SleepManager()

        self.optimizer = DatabaseOptimizer()

        self.cleaner = MemoryCleaner()

        self.running = False


    def status(self):

        return {

            "running": self.running,

            "sleeping": self.sleep.sleeping

        }


    async def start(self):

        self.running = True

        print("ORION Runtime aktif", flush=True)

        while self.running:

            health = self.health.check()

            if health["battery"] <= config.BATTERY_CRITICAL:

                print("Battery critical")

                self.sleep.sleep()

                await asyncio.sleep(

                    config.SLEEP_INTERVAL

                )

                continue


            result = await self.worker.run_once()

            if result["status"] == "idle":

                if config.AUTO_CLEAN_MEMORY:

                    self.cleaner.optimize()

                if config.AUTO_OPTIMIZE:

                    self.optimizer.optimize()

                await asyncio.sleep(

                    config.IDLE_INTERVAL

                )

            else:

                await asyncio.sleep(

                    config.RUNTIME_INTERVAL

                )


    def stop(self):

        self.running = False

        print(

            "Runtime stopped",

            flush=True

        )
