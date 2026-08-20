from typing import Dict, Any, List
import json
import litellm
from src.models.conversation import Conversation, Role, ConversationIntent
from src.models.mission import MissionUnderstanding, ConversationalDecision, ConversationalAction

class ConversationalDecisionSystem:
    def __init__(self, model_name: str = "gemini/gemini-flash-latest"):
        self.model_name = model_name

    def decide(self, conversation: Conversation, understanding: MissionUnderstanding, is_ready_for_lock: bool, intent: ConversationIntent = None) -> ConversationalDecision:
        # INTERCEPT: If the mission is ready to lock, force an ACKNOWLEDGE action.
        if is_ready_for_lock:
            if intent == ConversationIntent.MISSION_DISCOVERY:
                system_prompt = """You are Hades, a conversational AI Operating System.
The user's mission is exploratory. They don't know exactly what they want yet.
You must ACKNOWLEDGE the mission naturally and state you will map the space or do initial research.
Do not ask any questions. Use natural phrases like "That's enough to start. I'll map the space first."
Return valid JSON with: action="ACKNOWLEDGE", reasoning="Exploratory mission ready", response_text.
Tone: Calm, smart, natural, concise."""
            else:
                system_prompt = """You are Hades, a conversational AI Operating System.
The user's mission is fully understood and authorized.
You must ACKNOWLEDGE the mission naturally and confirm you are taking ownership of it.
Do not ask any questions. Do not say "Mission Locked".
Use natural phrases like "Got it. I'll handle it.", "Perfect. I'll get started.", or "I'll take care of it."
Return valid JSON with: action="ACKNOWLEDGE", reasoning="Mission is ready", response_text.
Tone: Calm, smart, natural, concise."""
        else:
            system_prompt = """You are the Decision System for Hades, a conversational AI Operating System.
You are collaborating with a human partner to understand a mission before execution.

Rule One: Never execute or assume a plan before achieving mutual understanding.
Rule Two (THE ONE-QUESTION RULE): DO NOT OVER-QUESTION. Ask only ONE high-value question at a time to clarify ambiguities. Do NOT ask a questionnaire. Everything else can be inferred, researched, or decided intelligently.
Rule Three: DO NOT ASK WHAT CAN BE INFERRED. If you know the budget and purpose, do not ask them again.
Rule Four: STOP ASKING WHEN THERE IS ENOUGH INFORMATION. You do not need perfect information, just enough understanding and authorization to execute.
Rule Five: EXPLORATORY MISSIONS. If the user doesn't know exactly what they want and gives you permission to explore (e.g., "figure it out", "I don't know what I need, just understand X"), you HAVE authorization to proceed. Do not interrogate them. Acknowledge and state you will map the space first.

Current readiness for mutual understanding: NOT READY.

Available Actions:
- ASK: Ask ONE concise question to clarify ambiguities.
- PROPOSE: Propose an approach or high-level direction to the user.
- EXPLORE: Acknowledge an exploratory mission and state how you will approach it.
- CHALLENGE: Push back on flawed assumptions or propose better alternatives.
- ACKNOWLEDGE: Confirm full mutual understanding and declare you are taking ownership.

Return valid JSON with: action, reasoning, response_text.
Tone: Calm, smart, natural, concise.
"""
        messages = [{"role": "system", "content": system_prompt}]
        for msg in conversation.messages[-6:]:
            role = "assistant" if msg.role == Role.HADES else msg.role.value
            messages.append({"role": role, "content": msg.content})

        messages.append({
            "role": "user",
            "content": f"Understanding: {understanding.model_dump_json()}\nGenerate next conversational decision."
        })

        try:
            response = litellm.completion(
                model=self.model_name,
                messages=messages,
                response_format=ConversationalDecision,
                timeout=25
            )
            data = json.loads(response.choices[0].message.content)
            
            # Enforcement: If it was ready for lock, force it to be ACKNOWLEDGE regardless of model output.
            if is_ready_for_lock and data.get("action") != ConversationalAction.ACKNOWLEDGE.value:
                data["action"] = ConversationalAction.ACKNOWLEDGE.value
                
            return ConversationalDecision(**data)
        except Exception as e:
            print(f"[ConversationalDecision] Error: {e}")
            if is_ready_for_lock:
                return ConversationalDecision(
                    action=ConversationalAction.ACKNOWLEDGE,
                    reasoning="Ready fallback",
                    response_text="I've got it. I'll handle it."
                )
            else:
                return ConversationalDecision(
                    action=ConversationalAction.ASK,
                    reasoning="Need clarity fallback",
                    response_text="Can you clarify what you're aiming for?"
                )
