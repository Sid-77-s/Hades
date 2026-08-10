import os
import uuid
from typing import Dict, Optional, Any
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from src.models.mission import Mission
from src.models.conversation import Conversation
from src.core.partner_brain import PartnerBrain
import litellm

load_dotenv()

app = FastAPI(title="Hades OS API")

# Initialize Partner Brain
brain = PartnerBrain()

# In-memory session storage for the demo
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
    is_error: bool = False

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = request.session_id
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = SessionState()
        
    session = sessions[session_id]
    
    # Simple prefixing for the user name context if provided
    context_prefix = ""
    if request.user_name and len(session.conversation.messages) == 0:
        context_prefix = f"[System Context: The user's name is {request.user_name}] "
        
    user_message = context_prefix + request.message
    
    try:
        # Process the message through Partner Brain
        updated_mission, response_text, decision = brain.process_message(
            session.mission, 
            session.conversation, 
            user_message
        )
        
        # Update the session state
        session.mission = updated_mission
        
        action_name = decision.action.value if decision and decision.action else None
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            mission_status=updated_mission.status.value,
            action=action_name,
            is_error=False
        )
    except litellm.RateLimitError as e:
        print(f"RateLimitError: {e}")
        return ChatResponse(
            response="I couldn't reach my reasoning service right now. Nothing was changed. Try again.",
            session_id=session_id,
            mission_status=session.mission.status.value,
            is_error=True
        )
    except Exception as e:
        print(f"Error processing chat: {e}")
        return ChatResponse(
            response="I couldn't reach my reasoning service right now. Nothing was changed. Try again.",
            session_id=session_id,
            mission_status=session.mission.status.value,
            is_error=True
        )

# Ensure static directory exists
os.makedirs("static", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)

# Mount the static files for the frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
