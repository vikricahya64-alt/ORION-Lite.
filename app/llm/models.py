from dataclasses import dataclass
from typing import Optional


@dataclass
class ChatMessage:
    role: str
    content: str
    name: Optional[str] = None

    def to_dict(self):
        data = {
            "role": self.role,
            "content": self.content,
        }

        if self.name:
            data["name"] = self.name

        return data
