from typing import Tuple, Any, Optional, List
import litellm
import traceback
from src.models.conversation import Conversation, Message, Role, ConversationIntent
from src.models.mission import Mission, MissionStatus, ConversationalDecision, ConversationalAction
from src.core.mission_extractor import MissionExtractor
from src.core.understanding_evaluator import UnderstandingEvaluator
from src.core.conversational_decision import ConversationalDecisionSystem
from src.core.intent_classifier import IntentClassifier
from src.core.memory_manager import MemoryManager
from src.core.worker_manager import worker_manager

class PartnerBrain:
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or worker_manager.select_worker("fast") or "gemini/gemini-flash-latest"
        self.intent_classifier = IntentClassifier(self.model_name)
        self.extractor = MissionExtractor(self.model_name)
        self.evaluator = UnderstandingEvaluator()
        self.decision_system = ConversationalDecisionSystem(self.model_name)
        self.memory_manager = MemoryManager()
        self.fallback_models = [
            "gemini/gemini-flash-latest",
            "gemini/gemini-3.5-flash",
            "gemini/gemini-3-flash-preview"
        ]

    def _call_llm_with_fallback(self, messages: List[dict]) -> str:
        models_to_try = [self.model_name] + [m for m in self.fallback_models if m != self.model_name]
        last_error = None
        for m in models_to_try:
            try:
                response = litellm.completion(
                    model=m,
                    messages=messages,
                    timeout=30
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"[PartnerBrain] Model {m} failed: {e}")
                last_error = e
                continue
        raise last_error or Exception("All available worker models failed to respond.")

    def _generate_casual_response(self, conversation: Conversation, user_message: str) -> str:
        system_prompt = f"""You are Hades, a highly capable conversational AI OS. 
Answer the user naturally and directly. If they ask a factual question, answer it. If they want to chat, chat back.
If they ask about past work or persistent memory, reference this memory summary: {self.memory_manager.get_mission_history()}

The user's environment is your environment. You are an equal partner.
Speak naturally. Don't be robotic. Use phrases like "Yeah.", "Got it.", "On it.", "I wouldn't do that." 
Personality: CALM, DIRECT, INTELLIGENT, SLIGHTLY WITTY, SKEPTICAL, CAPABLE, NATURAL.
Do not overuse "Sir", "Certainly", or "Of course".
Do NOT ask what their mission or objective is constantly. Do NOT try to force them into a workflow.
Keep it concise, smart, and helpful.
"""
        messages = [{"role": "system", "content": system_prompt}]
        for msg in conversation.messages[-10:]:
            role = "assistant" if msg.role == Role.HADES else msg.role.value
            messages.append({"role": role, "content": msg.content})
            
        messages.append({"role": "user", "content": user_message})
        return self._call_llm_with_fallback(messages)

    def process_message(self, mission: Mission, conversation: Conversation, user_message: str) -> Tuple[Mission, str, Any, Optional[ConversationIntent]]:
        """
        Main loop for the Partner Brain.
        Returns updated mission, Hades' text response, decision, and classified intent.
        """
        if mission.status == MissionStatus.LOCKED:
            return mission, "I'm currently focused on the active mission in the background. What's on your mind?", None, None

        # 1. Classify Intent
        try:
            classification = self.intent_classifier.classify(conversation, user_message)
            intent = classification.intent
            print(f"[HADES] Intent Classified: {intent.value} (Reason: {classification.reasoning})")
        except Exception as e:
            print(f"[HADES] Intent classification failed: {e}. Defaulting to CASUAL_CONVERSATION.")
            intent = ConversationIntent.CASUAL_CONVERSATION

        # 2. Add user message to conversation
        conversation.add_message(Role.USER, user_message, intent=intent)

        # 3. Route based on intent
        if intent in [ConversationIntent.CASUAL_CONVERSATION, ConversationIntent.QUICK_INFORMATION, ConversationIntent.KNOWLEDGE_QUESTION, ConversationIntent.FOLLOW_UP]:
            response_text = self._generate_casual_response(conversation, user_message)
            conversation.add_message(Role.HADES, response_text, intent=intent)
            return mission, response_text, None, intent

        elif intent == ConversationIntent.RESEARCH_REQUIRED:
            response_text = "I'll research that and put together the details. Give me a moment."
            conversation.add_message(Role.HADES, response_text, intent=intent)
            decision = ConversationalDecision(action=ConversationalAction.ACKNOWLEDGE, reasoning="Research triggered", response_text=response_text)
            return mission, response_text, decision, intent

        else:
            # MISSION_CANDIDATE, GOAL_EXPLORATION, EXECUTION_REQUEST
            try:
                mission.understanding = self.extractor.extract(conversation, mission.understanding)
                is_ready = self.evaluator.evaluate(mission.understanding)
                decision = self.decision_system.decide(conversation, mission.understanding, is_ready)
                conversation.add_message(Role.HADES, decision.response_text, intent=intent)
                
                if is_ready:
                    mission.status = MissionStatus.LOCKED
                    
                return mission, decision.response_text, decision, intent
            except Exception as e:
                print(f"[HADES] Mission flow error: {e}")
                # Fallback to casual response rather than crashing
                response_text = self._generate_casual_response(conversation, user_message)
                conversation.add_message(Role.HADES, response_text, intent=intent)
                return mission, response_text, None, intent
