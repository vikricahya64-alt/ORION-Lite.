from datetime import datetime
from device_monitor import DeviceMonitor


class AdaptiveController:


    def __init__(self):

        self.cycle = 0

        self.start_time = datetime.now()

        self.device = DeviceMonitor()

        self.last_mode = "active"



    def evaluate(self, system_state=None):


        self.cycle += 1



        # ======================
        # DEVICE REAL DATA
        # ======================

        if system_state is None:

            system_state = (
                self.device
                .device_state()
            )



        battery = int(
            system_state.get(
                "battery",
                100
            )
        )



        charging = (
            system_state
            .get(
                "status",
                "UNKNOWN"
            )
        )



        temperature = float(
            system_state.get(
                "temperature",
                0
            )
        )



        cpu_load = float(
            system_state.get(
                "cpu_load",
                0
            )
        )



        storage = int(
            system_state.get(
                "storage",
                0
            )
        )



        elapsed = (
            datetime.now()
            -
            self.start_time
        ).total_seconds()/60





        # ======================
        # EMERGENCY BATTERY
        # ======================


        if battery <=10 and charging != "CHARGING":

            self.last_mode="emergency"


            return {

                "allow":False,

                "mode":
                "emergency",

                "reason":
                "critical_battery",

                "action":
                "save_memory_stop_heavy_task",

                "battery":
                battery,

                "time":
                datetime.now().isoformat()

            }





        # ======================
        # LOW BATTERY
        # ======================


        if battery <=20 and charging != "CHARGING":


            self.last_mode="limited"


            return {


                "allow":False,

                "mode":
                "limited",

                "reason":
                "battery_low",

                "action":
                "reduce_activity",

                "battery":
                battery,

                "time":
                datetime.now().isoformat()

            }





        # ======================
        # TEMPERATURE
        # ======================


        if temperature >=45:


            self.last_mode="cooldown"


            return {


                "allow":False,


                "mode":
                "cooldown",


                "reason":
                "device_hot",


                "action":
                "wait_cooling",


                "temperature":
                temperature,


                "time":
                datetime.now().isoformat()

            }





        # ======================
        # CPU
        # ======================


        if cpu_load >=80:


            self.last_mode="cooldown"


            return {


                "allow":False,


                "mode":
                "cooldown",


                "reason":
                "cpu_high",


                "action":
                "reduce_worker",


                "cpu":
                cpu_load,


                "time":
                datetime.now().isoformat()

            }





        # ======================
        # STORAGE
        # ======================


        if storage >=90:


            self.last_mode="maintenance"


            return {


                "allow":True,


                "mode":
                "maintenance",


                "reason":
                "storage_high",


                "action":
                "cleanup_required",


                "storage":
                storage,


                "time":
                datetime.now().isoformat()

            }





        # ======================
        # LONG RUN PROTECTION
        # ======================


        if elapsed >=120:


            self.last_mode="sleep"


            return {


                "allow":False,


                "mode":
                "sleep",


                "reason":
                "runtime_limit",


                "time":
                datetime.now().isoformat()

            }





        # ======================
        # NORMAL
        # ======================


        self.last_mode="active"


        return {


            "allow":True,


            "mode":
            "active",


            "reason":
            "normal",


            "battery":
            battery,


            "temperature":
            temperature,


            "cpu_load":
            cpu_load,


            "storage":
            storage,


            "cycle":
            self.cycle,


            "elapsed_minutes":
            round(elapsed,2),


            "time":
            datetime.now().isoformat()

        }
