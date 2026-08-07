import subprocess


class AppLauncherAction:

    INTENTS = {

        "settings":
        "android.settings.SETTINGS",

        "wifi":
        "android.settings.WIFI_SETTINGS",

        "battery":
        "android.settings.BATTERY_SAVER_SETTINGS",

        "display":
        "android.settings.DISPLAY_SETTINGS",

        "storage":
        "android.settings.INTERNAL_STORAGE_SETTINGS",

        "bluetooth":
        "android.settings.BLUETOOTH_SETTINGS"
    }

    def execute(self, target):

        action = self.INTENTS.get(target)

        if action is None:

            return {
                "success": False,
                "error": f"Unknown target: {target}"
            }

        try:

            result = subprocess.run(

                [
                    "am",
                    "start",
                    "-a",
                    action
                ],

                capture_output=True,
                text=True

            )

            return {

                "success": result.returncode == 0,

                "action": "open_settings",

                "target": target,

                "stdout": result.stdout.strip(),

                "stderr": result.stderr.strip(),

                "exit_code": result.returncode

            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)

            }
