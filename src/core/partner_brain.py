from typing import Tuple, Any
from src.models.conversation import Conversation, Message, Role
from src.models.mission import Mission, MissionStatus
from src.core.mission_extractor import MissionExtractor
from src.core.understanding_evaluator import UnderstandingEvaluator
from src.core.conversational_decision import ConversationalDecisionSystem

class PartnerBrain:
    def __init__(self, model_name: str = "gemini/gemini-1.5-flash"):
        self.extractor = MissionExtractor(model_name)
        self.evaluator = UnderstandingEvaluator()
        self.decision_system = ConversationalDecisionSystem(model_name)

    def process_message(self, mission: Mission, conversation: Conversation, user_message: str) -> Tuple[Mission, str, Any]:
        """
        Main loop for the Partner Brain.
        Takes the current mission state, the conversation history, and the new user message.
        Returns the updated mission, Hades' text response, and the conversational decision.
        """
        if mission.status == MissionStatus.LOCKED:
            return mission, "Mission is already locked.", None

        # 1. Add user message to conversation
        conversation.add_message(Role.USER, user_message)
        
        # 2. Update understanding (Extractor)
        mission.understanding = self.extractor.extract(conversation, mission.understanding)
        
        # 3. Evaluate if we are ready for lock (Evaluator)
        is_ready = self.evaluator.evaluate(mission.understanding)
        
        # 4. Decide next action and generate response (Decision System)
        decision = self.decision_system.decide(conversation, mission.understanding, is_ready)
        
        # 5. Add Hades response to conversation
        conversation.add_message(Role.HADES, decision.response_text)
        
        # 6. If we evaluated as ready and the action was ACKNOWLEDGE, we might transition to LOCKED.
        # Wait, the Evaluator already checks `mutual_understanding_reached` which is set by the Extractor.
        # If is_ready is True, it means the user explicitly agreed with our summary in the PREVIOUS step,
        # OR they agreed in this step (Extractor saw "Yes" and set mutual_understanding_reached = True).
        # Since is_ready is True, we can safely lock.
        if is_ready:
            mission.status = MissionStatus.LOCKED
            
        return mission, decision.response_text, decision
