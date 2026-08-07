import subprocess


class TTSAction:

    def execute(self, message):

        try:
            result = subprocess.run(
                [
                    "termux-tts-speak",
                    message
                ],
                capture_output=True,
                text=True
            )

            return {
                "success": result.returncode == 0,
                "action": "tts",
                "message": message,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "exit_code": result.returncode
            }

        except Exception as e:

            return {
                "success": False,
                "action": "tts",
                "error": str(e)
            }
