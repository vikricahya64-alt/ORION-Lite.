import subprocess


class VibrationAction:

    def execute(self, duration=500):

        try:
            result = subprocess.run(
                [
                    "termux-vibrate",
                    "-d",
                    str(duration)
                ],
                capture_output=True,
                text=True
            )

            return {
                "success": result.returncode == 0,
                "action": "vibration",
                "duration": duration,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "exit_code": result.returncode
            }

        except Exception as e:

            return {
                "success": False,
                "action": "vibration",
                "error": str(e)
            }
