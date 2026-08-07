class ActionRouter:


    def __init__(self):

        from notification_action import NotificationAction
        from tts_action import TTSAction
        from vibration_action import VibrationAction
        from app_launcher_action import AppLauncherAction


        self.notify = NotificationAction()
        self.tts = TTSAction()
        self.vibrate = VibrationAction()
        self.launcher = AppLauncherAction()



    def execute(self,action):


        name = action.get("action")



        if name=="battery":


            self.notify.execute(
                "ORION",
                "Battery rendah. Mode perlindungan aktif"
            )


            self.tts.execute(
                "Battery rendah, silakan lakukan pengisian"
            )


            return self.launcher.execute(
                "battery"
            )



        if name=="temperature":


            self.notify.execute(
                "ORION",
                "Suhu perangkat tinggi"
            )


            self.vibrate.execute(500)


            return {
                "action":
                "temperature_warning"
            }



        if name=="storage":


            self.notify.execute(
                "ORION",
                "Penyimpanan hampir penuh"
            )


            return self.launcher.execute(
                "storage"
            )



        if name=="performance":


            self.notify.execute(
                "ORION",
                "CPU tinggi, mengurangi aktivitas"
            )


            return {
                "action":
                "performance_mode"
            }



        return {

            "action":
            "nothing"

        }
