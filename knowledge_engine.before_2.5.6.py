from memory import MemorySystem


class KnowledgeEngine:

    def __init__(self):

        self.memory = MemorySystem()


    def learn(
        self,
        topic,
        content
    ):

        return self.memory.remember(

            "knowledge",

            {

                "topic": topic,

                "content": content

            }

        )


    def search(
        self,
        keyword
    ):

        result = []

        data = self.memory.recall("knowledge")

        keyword = keyword.lower()

        for item in data:

            topic = item["data"].get(
                "topic",
                ""
            )

            content = item["data"].get(
                "content",
                ""
            )

            text = (

                str(topic)

                + " "

                + str(content)

            ).lower()

            if keyword in text:

                result.append(item)

        return result


    def topics(self):

        data = self.memory.recall("knowledge")

        return sorted(

            list(

                {

                    item["data"].get(
                        "topic",
                        "Unknown"
                    )

                    for item in data

                }

            )

        )


    def statistics(self):

        data = self.memory.recall("knowledge")

        return {

            "total": len(data),

            "topics": self.topics()

        }
