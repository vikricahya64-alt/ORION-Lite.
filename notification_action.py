import subprocess


class NotificationAction:

    def execute(self, title, message):

        try:

            result = subprocess.run(
                [
                    "termux-notification",
                    "--title", title,
                    "--content", message
                ],
                capture_output=True,
                text=True
            )

            return {
                "success": result.returncode == 0,
                "action": "notification",
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "exit_code": result.returncode
            }

        except Exception as e:

            return {
                "success": False,
                "action": "notification",
                "error": str(e)
            }
