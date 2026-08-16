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
- CASUAL_CONVERSATION: Greetings, small talk, chit chat, checking in, discussing philosophy, casual banter.
- QUICK_INFORMATION: Simple factual questions, weather, time, basic definitions, quick math.
- KNOWLEDGE_QUESTION: Explaining a concept, asking for opinions or advice.
- GOAL_EXPLORATION: Brainstorming, discussing project ideas, high level requests that need discussion.
- RESEARCH_REQUIRED: Explicitly asking Hades to search the web, lookup live data, or gather intelligence.
- MISSION_CANDIDATE: Complex multi-step task (e.g., build presentation, write and execute code, analyze datasets, automate workflow).
- EXECUTION_REQUEST: Explicit command to execute tools, run terminal scripts, or modify files.
- FOLLOW_UP: Clarifications or answers to Hades' previous questions.
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
            response = litellm.completion(
                model=self.model_name,
                messages=messages,
                response_format=IntentClassification,
                timeout=20
            )
            data = json.loads(response.choices[0].message.content)
            return IntentClassification(**data)
        except Exception as e:
            # Fallback
            lower = current_message.lower()
            if any(g in lower for g in ["hi", "hello", "hey", "hades", "what's up", "how are you", "who are you"]):
                return IntentClassification(intent=ConversationIntent.CASUAL_CONVERSATION, reasoning="Greeting", confidence=0.9)
            if "research" in lower or "search" in lower or "find out" in lower:
                return IntentClassification(intent=ConversationIntent.RESEARCH_REQUIRED, reasoning="Research keyword", confidence=0.8)
            return IntentClassification(intent=ConversationIntent.CASUAL_CONVERSATION, reasoning="Default fallback", confidence=0.5)
