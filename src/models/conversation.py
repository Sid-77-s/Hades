from enum import Enum
from pydantic import BaseModel
from typing import List

class Role(str, Enum):
    USER = "user"
    HADES = "hades"
    SYSTEM = "system"

class Message(BaseModel):
    role: Role
    content: str

class Conversation(BaseModel):
    messages: List[Message] = []

    def add_message(self, role: Role, content: str):
        self.messages.append(Message(role=role, content=content))
