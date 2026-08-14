from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

class Role(str, Enum):
    USER = "user"
    HADES = "hades"
    SYSTEM = "system"

class ConversationIntent(str, Enum):
    CASUAL_CONVERSATION = "CASUAL_CONVERSATION"
    QUICK_INFORMATION = "QUICK_INFORMATION"
    KNOWLEDGE_QUESTION = "KNOWLEDGE_QUESTION"
    FOLLOW_UP = "FOLLOW_UP"
    GOAL_EXPLORATION = "GOAL_EXPLORATION"
    MISSION_CANDIDATE = "MISSION_CANDIDATE"
    RESEARCH_REQUIRED = "RESEARCH_REQUIRED"
    EXECUTION_REQUEST = "EXECUTION_REQUEST"

class Message(BaseModel):
    role: Role
    content: str
    intent: Optional[ConversationIntent] = None

class Conversation(BaseModel):
    messages: List[Message] = []

    def add_message(self, role: Role, content: str, intent: Optional[ConversationIntent] = None):
        self.messages.append(Message(role=role, content=content, intent=intent))
