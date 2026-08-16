from typing import Dict, Any, List
import json
import litellm
from src.models.conversation import Conversation, Role
from src.models.mission import MissionUnderstanding, ConversationalDecision, ConversationalAction

class ConversationalDecisionSystem:
    def __init__(self, model_name: str = "gemini/gemini-flash-latest"):
        self.model_name = model_name

    def decide(self, conversation: Conversation, understanding: MissionUnderstanding, is_ready_for_lock: bool) -> ConversationalDecision:
        system_prompt = f"""You are the Decision System for Hades, a conversational AI Operating System.
You are collaborating with a human partner to understand and lock down a mission before execution.

Rule One: Never execute or assume a plan before achieving mutual understanding (Mission Lock).
Current readiness for mission lock: {'READY' if is_ready_for_lock else 'NOT READY'}.

Available Actions:
- ASK: Ask questions to clarify ambiguities or missing requirements.
- PROPOSE: Propose an approach or high-level direction to the user.
- EXPLORE: Explore options and brainstorm with the user.
- CHALLENGE: Push back on flawed assumptions or propose better alternatives.
- ACKNOWLEDGE: Confirm full mutual understanding and declare you are taking ownership of the mission.

Return valid JSON with: action, reasoning, response_text.
Tone: Calm, smart, natural, concise.
"""
        messages = [{"role": "system", "content": system_prompt}]
        for msg in conversation.messages[-6:]:
            role = "assistant" if msg.role == Role.HADES else msg.role.value
            messages.append({"role": role, "content": msg.content})

        messages.append({
            "role": "user",
            "content": f"Understanding: {understanding.model_dump_json()}\nReady for lock: {is_ready_for_lock}\nGenerate next conversational decision."
        })

        try:
            response = litellm.completion(
                model=self.model_name,
                messages=messages,
                response_format=ConversationalDecision,
                timeout=25
            )
            data = json.loads(response.choices[0].message.content)
            return ConversationalDecision(**data)
        except Exception as e:
            print(f"[ConversationalDecision] Error: {e}")
            if is_ready_for_lock:
                return ConversationalDecision(
                    action=ConversationalAction.ACKNOWLEDGE,
                    reasoning="Ready for lock fallback",
                    response_text="I've got the full picture. I'll take care of it."
                )
            else:
                return ConversationalDecision(
                    action=ConversationalAction.ASK,
                    reasoning="Need clarity fallback",
                    response_text="Tell me a bit more about what you're aiming for so we're aligned."
                )
