import os
import httpx

from .models import ChatMessage


class LLMClient:

    def __init__(self):

        self.provider = "openai"

        self.model = os.getenv(
            "LLM_MODEL",
            "gpt-5.5"
        )

        self.api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        self.url = (
            "https://api.openai.com/v1/chat/completions"
        )


        if not self.api_key:
            raise Exception(
                "OPENAI_API_KEY belum tersedia"
            )


    def chat(self, messages):

        formatted = []

        for message in messages:

            if isinstance(message, ChatMessage):

                formatted.append(
                    message.to_dict()
                )

            else:

                formatted.append(message)


        response = httpx.post(

            self.url,

            headers={

                "Authorization":
                f"Bearer {self.api_key}",

                "Content-Type":
                "application/json"

            },

            json={

                "model": self.model,

                "messages": formatted

            },

            timeout=60

        )


        data = response.json()


        if "error" in data:

            return {

                "status":"error",

                "message":
                data["error"]["message"]

            }


        return {

            "status":"success",

            "provider":self.provider,

            "model":self.model,

            "response":
            data["choices"][0]["message"]["content"]

        }


    def complete(self, prompt):

        result = self.chat([

            {

                "role":"user",

                "content":prompt

            }

        ])

        return result


    def planner(self, goal):

        return self.complete(

            f"Buat rencana langkah untuk: {goal}"

        )
