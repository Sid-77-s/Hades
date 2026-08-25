import json
import os
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime

MEMORY_FILE = "memory.json"

class MissionHistoryItem(BaseModel):
    mission_id: str
    objective: str
    status: str
    timestamp: str
    summary: str
    outputs: List[str] = Field(default_factory=list)

class HadesMemory(BaseModel):
    mission_history: List[MissionHistoryItem] = Field(default_factory=list)
    preferences: Dict[str, str] = Field(default_factory=dict)
    active_missions: Dict[str, Any] = Field(default_factory=dict) # Current serialized state

class MemoryManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryManager, cls).__new__(cls)
            cls._instance._load_memory()
        return cls._instance
        
    def _load_memory(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, 'r') as f:
                    data = json.load(f)
                    self.memory = HadesMemory(**data)
            except Exception as e:
                print(f"[MemoryManager] Error loading memory: {e}")
                self.memory = HadesMemory()
        else:
            self.memory = HadesMemory()
            
    def save_memory(self):
        with open(MEMORY_FILE, 'w') as f:
            f.write(self.memory.model_dump_json(indent=2))

    def add_mission_to_history(self, mission_id: str, objective: str, status: str, summary: str, outputs: List[str]):
        item = MissionHistoryItem(
            mission_id=mission_id,
            objective=objective,
            status=status,
            timestamp=datetime.now().isoformat(),
            summary=summary,
            outputs=outputs
        )
        self.memory.mission_history.append(item)
        self.save_memory()

    def get_mission_history(self) -> List[MissionHistoryItem]:
        return self.memory.mission_history
        
    def save_active_mission(self, mission_id: str, state: dict):
        self.memory.active_missions[mission_id] = state
        self.save_memory()
        
    def get_active_mission(self, mission_id: str) -> dict:
        return self.memory.active_missions.get(mission_id)
