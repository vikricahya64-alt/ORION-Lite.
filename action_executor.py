import os
import shutil
import subprocess
from datetime import datetime


class ActionExecutor:

    def __init__(self):
        self.termux = shutil.which("termux-notification") is not None

    # ------------------------
    # TERMUX NOTIFICATION
    # ------------------------

    def notify(self, title, message):

        if not self.termux:
            return False

        try:

            subprocess.run(
                [
                    "termux-notification",
                    "--title",
                    title,
                    "--content",
                    message
                ],
                check=False
            )

            return True

        except Exception:

            return False

    # ------------------------
    # OPEN APP
    # ------------------------

    def open_app(self, package_name):

        try:

            subprocess.run(
                [
                    "am",
                    "start",
                    "-n",
                    package_name
                ],
                check=False
            )

            return True

        except Exception:

            return False

    # ------------------------
    # CLEAN ORION CACHE
    # ------------------------

    def clean_orion_cache(self):

        cache = "cache"

        if not os.path.exists(cache):

            return {
                "success": True,
                "deleted": 0
            }

        deleted = 0

        for root, dirs, files in os.walk(cache):

            for f in files:

                try:

                    os.remove(os.path.join(root, f))

                    deleted += 1

                except Exception:

                    pass

        return {
            "success": True,
            "deleted": deleted
        }

    # ------------------------
    # CLEAN ORION LOGS
    # ------------------------

    def clean_logs(self):

        folder = "logs"

        if not os.path.exists(folder):

            return {
                "success": True,
                "deleted": 0
            }

        deleted = 0

        for root, dirs, files in os.walk(folder):

            for f in files:

                try:

                    os.remove(os.path.join(root, f))

                    deleted += 1

                except Exception:

                    pass

        return {
            "success": True,
            "deleted": deleted
        }

    # ------------------------
    # EXECUTE
    # ------------------------

    def execute(self, action):

        result = {
            "time": datetime.now().isoformat(),
            "action": action,
            "success": False
        }

        if action == "health_check":

            result["success"] = True

            return result

        elif action == "cleanup_cache":

            data = self.clean_orion_cache()

            result.update(data)

            return result

        elif action == "cleanup_logs":

            data = self.clean_logs()

            result.update(data)

            return result

        elif action == "notify":

            ok = self.notify(
                "ORION",
                "Autonomous action executed."
            )

            result["success"] = ok

            return result

        result["reason"] = "unknown action"

        return result
