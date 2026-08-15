import os
import uuid
import asyncio
import traceback
from typing import Dict, Optional, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from sse_starlette.sse import EventSourceResponse

from src.models.mission import Mission, MissionStatus
from src.models.conversation import Conversation
from src.core.partner_brain import PartnerBrain
from src.core.research_manager import ResearchManager
from src.models.conversation import ConversationIntent

# New Imports
from src.core.config_manager import ConfigManager
from src.core.memory_manager import MemoryManager
from src.core.event_bus import EventBus
from src.core.execution.execution_brain import ExecutionBrain
from src.core.execution.execution_brain import ExecutionBrain

load_dotenv()

# Initialize Core Managers
config_manager = ConfigManager()

# Ensure LiteLLM picks up the persisted key
if config_manager.get_credentials().gemini_key:
    os.environ["GEMINI_API_KEY"] = config_manager.get_credentials().gemini_key

memory_manager = MemoryManager()
event_bus = EventBus()

# Removed obsolete CapabilityRegistry initialization

app = FastAPI(title="Hades OS API")

# Initialize Brains
brain = PartnerBrain()
research_manager = ResearchManager()
execution_brain = ExecutionBrain()

class SessionState:
    def __init__(self):
        self.mission = Mission(id=str(uuid.uuid4()))
        self.conversation = Conversation()

sessions: Dict[str, SessionState] = {}

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_name: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    mission_status: str
    action: Optional[str] = None
    intent: Optional[str] = None
    is_error: bool = False
    developer_error: Optional[Dict[str, Any]] = None

@app.get("/api/events")
async def events_endpoint(request: Request):
    async def event_generator():
        q = await event_bus.subscribe()
        try:
            while True:
                if await request.is_disconnected():
                    break
                event = await q.get()
                yield {"data": event}
        finally:
            event_bus.unsubscribe(q)
    return EventSourceResponse(event_generator())

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = request.session_id
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = SessionState()
        
    session = sessions[session_id]
    user_message = request.message
    
    try:
        updated_mission, response_text, decision, intent = brain.process_message(
            session.mission, 
            session.conversation, 
            user_message
        )
        
        # If the mission just locked, trigger ExecutionBrain in background
        if updated_mission.status == MissionStatus.LOCKED and session.mission.status != MissionStatus.LOCKED:
            print("[main] Mission locked! Starting execution brain.")
            # We don't await this, let it run in background
            asyncio.create_task(execution_brain.process_mission(updated_mission))
            
        session.mission = updated_mission
        action_name = decision.action.value if decision and decision.action else None
        intent_name = intent.value if intent else None
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            mission_status=updated_mission.status.value,
            action=action_name,
            intent=intent_name,
            is_error=False
        )
    except Exception as e:
        print(f"[HADES] Error: {e}")
        traceback.print_exc()
        
        dev_err = {
            "provider": config_manager.get_settings().model_provider,
            "status": getattr(e, "status_code", 500),
            "reason": str(e),
            "type": e.__class__.__name__
        }
        
        natural_response = "I couldn't reach my core processing system just now."
        if "AuthenticationError" in dev_err["type"]:
            natural_response = "My access credentials appear to be invalid. Check the settings."
        elif "RateLimitError" in dev_err["type"]:
            natural_response = "I'm receiving too many requests right now. Give me a moment."
            
        return ChatResponse(
            response=natural_response,
            session_id=session_id,
            mission_status=session.mission.status.value,
            is_error=True,
            developer_error=dev_err
        )

from src.skills.registry import registry as skill_registry

@app.get("/api/config/status")
async def get_config_status():
    """Returns the health status of all skills to power the Settings UI."""
    skill_registry.discover_skills()
    skills = skill_registry.get_all_skills()
    
    status_map = {}
    for skill in skills:
        status_map[skill.metadata.skill_id] = {
            "name": skill.metadata.name,
            "status": skill.metadata.health_status,
            "category": skill.metadata.category
        }
        
    return {"skills": status_map}

@app.get("/api/memory")
async def get_memory():
    return memory_manager.get_mission_history()

@app.post("/api/execution/recover")
async def execution_recover(data: dict):
    # Endpoint to allow frontend to authorize fallback
    mission_id = data.get("mission_id")
    print(f"[main] User authorized fallback for mission {mission_id}")
    event_bus.publish_sync("RECOVERY_STARTED", {"mission_id": mission_id, "message": "Switching to fallback..."})
    return {"status": "ok"}

os.makedirs("static", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
