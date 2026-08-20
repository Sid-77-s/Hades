from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

class Role(str, Enum):
    USER = "user"
    HADES = "hades"
    SYSTEM = "system"

class ConversationIntent(str, Enum):
    CASUAL = "CASUAL"
    SIMPLE_REQUEST = "SIMPLE_REQUEST"
    SMALL_TASK = "SMALL_TASK"
    REAL_MISSION = "REAL_MISSION"
    MISSION_DISCOVERY = "MISSION_DISCOVERY"

class Message(BaseModel):
    role: Role
    content: str
    intent: Optional[ConversationIntent] = None

class Conversation(BaseModel):
    messages: List[Message] = []

    def add_message(self, role: Role, content: str, intent: Optional[ConversationIntent] = None):
        self.messages.append(Message(role=role, content=content, intent=intent))
