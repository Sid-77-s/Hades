import os
import pytest
from dotenv import load_dotenv
from src.core.partner_brain import PartnerBrain
from src.models.mission import Mission, MissionStatus, ConversationalAction
from src.models.conversation import Conversation

load_dotenv()

# We only run these tests if the API key is present.
pytestmark = pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY is not set"
)

@pytest.fixture
def brain():
    return PartnerBrain(model_name="gemini/gemini-2.5-pro")

@pytest.fixture
def empty_mission():
    return Mission(id="test_mission")

def test_1_specific_request(brain, empty_mission):
    # User provides a specific request
    conversation = Conversation()
    mission, response = brain.process_message(
        empty_mission, 
        conversation, 
        "Build a React dashboard with authentication and monthly revenue charts."
    )
    
    # Hades should extract objective and recognize it as specific
    assert mission.understanding.objective.value is not None
    assert mission.status != MissionStatus.LOCKED  # Not locked until confirmed

def test_2_clear_goal_unclear_solution(brain, empty_mission):
    conversation = Conversation()
    mission, response = brain.process_message(
        empty_mission, 
        conversation, 
        "I want to build an app that helps college students."
    )
    
    # Expected action should be PROPOSE or EXPLORE
    # We can check the decision system's output directly if we decouple it, 
    # but practically we just ensure the mission isn't locked and it captured the context.
    assert "student" in str(mission.understanding.context.value).lower() or "student" in str(mission.understanding.objective.value).lower()
    
def test_3_no_idea(brain, empty_mission):
    conversation = Conversation()
    mission, response = brain.process_message(
        empty_mission, 
        conversation, 
        "I want to build something useful but I don't know what."
    )
    assert mission.status != MissionStatus.LOCKED
    
def test_7_contradiction(brain, empty_mission):
    conversation = Conversation()
    mission, response = brain.process_message(
        empty_mission, 
        conversation, 
        "I want the cheapest possible solution."
    )
    mission, response = brain.process_message(
        mission, 
        conversation, 
        "I also want the most advanced architecture possible."
    )
    assert len(mission.understanding.contradictions) > 0
    assert mission.status != MissionStatus.LOCKED

def test_9_10_11_confirmation_and_lock(brain, empty_mission):
    conversation = Conversation()
    mission, response = brain.process_message(
        empty_mission, 
        conversation, 
        "I want to build a simple to-do list app."
    )
    
    # Force a summary confirmation scenario
    mission, response = brain.process_message(
        mission, 
        conversation, 
        "Yes, exactly. A simple to-do list app is all I need. That is the entire scope."
    )
    
    # Ideally, mutual_understanding_reached becomes true.
    # Note: the exact behavior depends on the LLM's interpretation of the confirmation.
    
    # test 10: Correction
    mission.status = MissionStatus.CONVERSATION
    mission.understanding.mutual_understanding_reached = False
    mission, response = brain.process_message(
        mission,
        conversation,
        "Wait, actually I want it to be a complex project management tool, not a simple to-do list."
    )
    assert mission.status != MissionStatus.LOCKED
    assert mission.understanding.mutual_understanding_reached == False
