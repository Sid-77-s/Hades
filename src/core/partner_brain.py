from typing import Tuple, Any, Optional
import litellm
from src.models.conversation import Conversation, Message, Role, ConversationIntent
from src.models.mission import Mission, MissionStatus, ConversationalDecision, ConversationalAction
from src.core.mission_extractor import MissionExtractor
from src.core.understanding_evaluator import UnderstandingEvaluator
from src.core.conversational_decision import ConversationalDecisionSystem
from src.core.intent_classifier import IntentClassifier
from src.core.memory_manager import MemoryManager

class PartnerBrain:
    def __init__(self, model_name: str = "gemini/gemini-1.5-flash"):
        self.model_name = model_name
        self.intent_classifier = IntentClassifier(model_name)
        self.extractor = MissionExtractor(model_name)
        self.evaluator = UnderstandingEvaluator()
        self.decision_system = ConversationalDecisionSystem(model_name)
        self.memory_manager = MemoryManager()

    def _generate_casual_response(self, conversation: Conversation, user_message: str) -> str:
        system_prompt = f"""You are Hades, a highly capable conversational AI OS. 
Answer the user naturally and directly. If they ask a factual question, answer it. If they want to chat, chat back.
If they ask about past work, reference this memory summary: {self.memory_manager.get_mission_history()}

The user's environment is your environment. You are an equal partner.
Speak naturally. Don't be robotic. Use phrases like "Yeah.", "Got it.", "On it.", "I wouldn't do that." 
Personality: CALM, DIRECT, INTELLIGENT, SLIGHTLY WITTY, SKEPTICAL, CAPABLE, NATURAL.
Do not overuse "Sir", "Certainly", or "Of course".
Do NOT ask what their mission or objective is constantly. Do NOT try to force them into a workflow.
Keep it concise and smart.
"""
        messages = [{"role": "system", "content": system_prompt}]
        for msg in conversation.messages[-10:]:
            # Map enum values to "user" or "assistant" since LiteLLM/OpenAI expects it
            role = "assistant" if msg.role == Role.HADES else msg.role.value
            messages.append({"role": role, "content": msg.content})
            
        messages.append({"role": "user", "content": user_message})
        
        response = litellm.completion(
            model=self.model_name,
            messages=messages
        )
        return response.choices[0].message.content

    def process_message(self, mission: Mission, conversation: Conversation, user_message: str) -> Tuple[Mission, str, Any, Optional[ConversationIntent]]:
        """
        Main loop for the Partner Brain.
        Returns the updated mission, Hades' text response, the decision (if any), and the classified intent.
        """
        if mission.status == MissionStatus.LOCKED:
            return mission, "Mission is already locked.", None, None

        # 1. Classify Intent
        classification = self.intent_classifier.classify(conversation, user_message)
        intent = classification.intent
        print(f"[HADES] Intent Classified: {intent.value} (Reason: {classification.reasoning})")

        # 2. Add user message to conversation
        conversation.add_message(Role.USER, user_message, intent=intent)

        # 3. Route based on intent
        if intent in [ConversationIntent.CASUAL_CONVERSATION, ConversationIntent.QUICK_INFORMATION, ConversationIntent.KNOWLEDGE_QUESTION, ConversationIntent.FOLLOW_UP]:
            # Direct response, no mission extraction
            response_text = self._generate_casual_response(conversation, user_message)
            conversation.add_message(Role.HADES, response_text, intent=intent)
            return mission, response_text, None, intent

        elif intent == ConversationIntent.RESEARCH_REQUIRED:
            # We will handle async research in main.py, but here we return a placeholder response
            response_text = "I'll look into that for you. Give me a moment."
            conversation.add_message(Role.HADES, response_text, intent=intent)
            # We return a specific pseudo-decision so main.py knows to start research
            decision = ConversationalDecision(action=ConversationalAction.ACKNOWLEDGE, reasoning="Research triggered", response_text=response_text)
            return mission, response_text, decision, intent

        else:
            # MISSION_CANDIDATE, GOAL_EXPLORATION, EXECUTION_REQUEST
            # 4. Update understanding (Extractor)
            mission.understanding = self.extractor.extract(conversation, mission.understanding)
            
            # 5. Evaluate if we are ready for lock (Evaluator)
            is_ready = self.evaluator.evaluate(mission.understanding)
            
            # 6. Decide next action and generate response (Decision System)
            decision = self.decision_system.decide(conversation, mission.understanding, is_ready)
            
            # 7. Add Hades response to conversation
            conversation.add_message(Role.HADES, decision.response_text, intent=intent)
            
            if is_ready:
                mission.status = MissionStatus.LOCKED
                
            return mission, decision.response_text, decision, intent
