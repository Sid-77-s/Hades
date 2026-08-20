import asyncio
import os
from src.core.partner_brain import PartnerBrain
from src.models.conversation import Conversation
from src.models.mission import Mission, MissionStatus

# Force lightweight local models if available, or just mock the LLM calls if needed.
# We'll use the default setup, so make sure GEMINI_API_KEY is loaded (main.py does it, let's just rely on the env if running from CLI).
from dotenv import load_dotenv
load_dotenv()

async def run_tests():
    print("=== HADES BEHAVIORAL CORE TEST RUN ===")
    
    brain = PartnerBrain()
    
    scenarios = [
        ("TEST 1 - CASUAL", "Hey Hades."),
        ("TEST 2 - SIMPLE QUESTION", "What is an API?"),
        ("TEST 3 - SMALL TASK", "Create a folder called Hades Test."),
        ("TEST 4 - AMBIGUOUS SMALL TASK", "Make this better."),
        ("TEST 5 - REAL MISSION", "Research the AI OS market."),
        ("TEST 6 - USER HAS CLEAR PURPOSE", "Research AI OS competitors so I can position Hades for investors."),
        ("TEST 7 - USER DOESN'T KNOW", "I don't really know what I need. I just want to understand AI operating systems."),
    ]
    
    for name, user_msg in scenarios:
        print(f"\n--- {name} ---")
        mission = Mission(id="test_id")
        conversation = Conversation()
        
        print(f"USER: {user_msg}")
        updated_mission, response, decision, intent = brain.process_message(mission, conversation, user_msg)
        print(f"INTENT: {intent.value if intent else 'None'}")
        print(f"STATUS: {updated_mission.status.value}")
        print(f"HADES: {response}")

if __name__ == "__main__":
    asyncio.run(run_tests())
