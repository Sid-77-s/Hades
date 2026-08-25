from typing import Dict, Any, List
import json
import litellm
from pydantic import BaseModel
from src.models.conversation import Conversation, Role, ConversationIntent

class IntentClassification(BaseModel):
    intent: ConversationIntent
    reasoning: str
    confidence: float

class IntentClassifier:
    def __init__(self, model_name: str = "gemini/gemini-flash-latest"):
        self.model_name = model_name

    def classify(self, conversation: Conversation, current_message: str) -> IntentClassification:
        system_prompt = """You are an intent classifier for Hades, an AI Operating System.
Classify the user's intent based on their latest message and recent conversation history.

Available Intents:
- CASUAL: Greetings, small talk, chit chat, philosophy, banter. Do NOT classify as a mission.
- SIMPLE_REQUEST: Factual questions, weather, time, basic definitions, quick math. No action required, just answering.
- SMALL_TASK: Small actionable tasks (e.g., "Create a folder", "Make this shorter", "Find the OpenAI docs"). Handled efficiently without long alignment.
- REAL_MISSION: Substantial tasks where misunderstanding wastes time/resources (e.g., "Research AI OS market", "Build a website"). Requires mutual alignment first.
- MISSION_DISCOVERY: The user wants something but doesn't know exactly what, giving you permission to explore (e.g., "I don't know what I need, just help me understand X", "Explore this").
"""
        messages = [{"role": "system", "content": system_prompt}]
        for msg in conversation.messages[-4:]:
            role = "assistant" if msg.role == Role.HADES else msg.role.value
            messages.append({"role": role, "content": msg.content})

        messages.append({
            "role": "user", 
            "content": f"Classify the following user message:\nMessage: '{current_message}'\n\nReturn JSON with keys: intent, reasoning, confidence."
        })

        try:
            from src.core.worker_manager import worker_manager
            response = worker_manager.complete(
                messages=messages,
                capability="conversational",
                response_format={"type": "json_object"},
                timeout=20
            )
            data = json.loads(response.choices[0].message.content)
            return IntentClassification(**data)
        except Exception as e:
            # Fallback
            lower = current_message.lower()
            if any(g in lower for g in ["hi", "hello", "hey", "hades", "what's up"]):
                return IntentClassification(intent=ConversationIntent.CASUAL, reasoning="Greeting", confidence=0.9)
            if "research" in lower or "build" in lower or "plan" in lower or "analyze" in lower:
                return IntentClassification(intent=ConversationIntent.REAL_MISSION, reasoning="Mission keyword", confidence=0.7)
            if "explore" in lower or "figure it out" in lower:
                return IntentClassification(intent=ConversationIntent.MISSION_DISCOVERY, reasoning="Exploration keyword", confidence=0.8)
            return IntentClassification(intent=ConversationIntent.CASUAL, reasoning="Default fallback", confidence=0.5)
