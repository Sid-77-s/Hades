import os
import json
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CONFIG_FILE = "config.json"

class APICredentials(BaseModel):
    gemini_key: Optional[str] = None
    openai_key: Optional[str] = None
    gamma_email: Optional[str] = None
    gamma_password: Optional[str] = None
    search_api_key: Optional[str] = None

class AppSettings(BaseModel):
    model_provider: str = "gemini"
    allow_background_execution: bool = True
    notifications_level: str = "BETTER_IDEA" # SILENT, BETTER_IDEA, BLOCKER, MEANINGFUL_DECISION, COMPLETE

class HadesConfig(BaseModel):
    settings: AppSettings = Field(default_factory=AppSettings)
    # Note: api_credentials is removed from the JSON config to prevent accidental save
    
class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.config = HadesConfig()
            cls._instance.api_credentials = APICredentials()
            cls._instance._load_config()
        return cls._instance
        
    def _load_config(self):
        # 1. Load app settings from config.json (non-sensitive)
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    if 'settings' in data:
                        self.config.settings = AppSettings(**data['settings'])
            except Exception as e:
                print(f"[ConfigManager] Error loading config: {e}")
                
        # 2. Load API credentials ONLY from environment variables (.env)
        self.api_credentials.gemini_key = os.getenv("GEMINI_API_KEY", "").strip().strip('"').strip("'") or None
        self.api_credentials.openai_key = os.getenv("OPENAI_API_KEY", "").strip().strip('"').strip("'") or None
        self.api_credentials.gamma_email = os.getenv("GAMMA_EMAIL", "").strip() or None
        self.api_credentials.gamma_password = os.getenv("GAMMA_PASSWORD", "").strip() or None
        self.api_credentials.search_api_key = os.getenv("SEARCH_API_KEY", "").strip() or None
            
    def save_config(self):
        # Only save non-sensitive settings to config.json
        with open(CONFIG_FILE, 'w') as f:
            f.write(self.config.model_dump_json(indent=2))

    def get_credentials(self) -> APICredentials:
        return self.api_credentials

    def get_settings(self) -> AppSettings:
        return self.config.settings
