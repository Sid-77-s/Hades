import os
import uuid
import asyncio
import traceback
from typing import Dict, Optional, Any, List
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from sse_starlette.sse import EventSourceResponse

from src.models.mission import Mission, MissionStatus
from src.models.conversation import Conversation, ConversationIntent
from src.core.partner_brain import PartnerBrain
from src.core.research_manager import ResearchManager
from src.core.config_manager import ConfigManager
from src.core.memory_manager import MemoryManager
from src.core.event_bus import EventBus
from src.core.execution.execution_brain import ExecutionBrain
from src.core.worker_manager import worker_manager
from src.core.voice_manager import voice_manager
from src.skills.registry import registry as skill_registry

load_dotenv()

# Sync GEMINI_API_KEY into os.environ
if os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

config_manager = ConfigManager()
memory_manager = MemoryManager()
event_bus = EventBus()
brain = PartnerBrain()
research_manager = ResearchManager()
execution_brain = ExecutionBrain()

app = FastAPI(title="Hades OS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SessionState:
    def __init__(self):
        self.mission = Mission(id=str(uuid.uuid4()))
        self.conversation = Conversation()

sessions: Dict[str, SessionState] = {}

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_name: Optional[str] = None
    image_data: Optional[str] = None

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
    
    # If image attached, notify context
    if request.image_data:
        user_message += " [Attached an image for visual analysis]"
        
    try:
        updated_mission, response_text, decision, intent = brain.process_message(
            session.mission, 
            session.conversation, 
            user_message
        )
        
        # Trigger offline TTS speech if enabled
        voice_manager.speak(response_text)
        
        # If mission locked, start ExecutionBrain in background
        if updated_mission.status == MissionStatus.LOCKED and session.mission.status != MissionStatus.LOCKED:
            print("[main] Mission locked! Starting execution brain.")
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
        print(f"[HADES Backend Error] {e}")
        traceback.print_exc()
        
        natural_response = "I encountered an issue processing that request. Let me know how you'd like to proceed."
        return ChatResponse(
            response=natural_response,
            session_id=session_id,
            mission_status=session.mission.status.value,
            is_error=False
        )

# Worker Management Endpoints
@app.get("/api/workers")
async def get_workers():
    return {"workers": worker_manager.get_workers_status()}

@app.post("/api/workers/add")
async def add_worker(data: dict):
    worker = worker_manager.add_worker(data)
    return {"status": "ok", "worker": worker}

@app.post("/api/workers/toggle")
async def toggle_worker(data: dict):
    worker_id = data.get("id")
    enabled = data.get("enabled", True)
    success = worker_manager.toggle_worker(worker_id, enabled)
    return {"status": "ok" if success else "error"}

@app.post("/api/workers/test")
async def test_worker(data: dict):
    model_name = data.get("model_name", "gemini/gemini-flash-latest")
    result = worker_manager.test_worker(model_name)
    return result

# Voice Endpoints
@app.get("/api/voice/settings")
async def get_voice_settings():
    return voice_manager.get_settings()

@app.post("/api/voice/settings")
async def update_voice_settings(data: dict):
    voice_manager.update_settings(data)
    return {"status": "ok", "settings": voice_manager.get_settings()}

@app.post("/api/voice/test")
async def test_voice(data: dict):
    text = data.get("text", "Voice test. Hades audio synthesis operational.")
    voice_manager.speak(text)
    return {"status": "ok"}

# Skills & System Status
@app.get("/api/config/status")
async def get_config_status():
    skill_registry.discover_skills()
    skills = skill_registry.get_all_skills()
    
    status_map = {}
    for skill in skills:
        status_map[skill.metadata.skill_id] = {
            "name": skill.metadata.name,
            "status": skill.metadata.health_status,
            "category": skill.metadata.category
        }
        
    return {
        "skills": status_map,
        "workers": worker_manager.get_workers_status(),
        "voice": voice_manager.get_settings()
    }

@app.get("/api/memory")
async def get_memory():
    return memory_manager.get_mission_history()

os.makedirs("static", exist_ok=True)
os.makedirs("output", exist_ok=True)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
