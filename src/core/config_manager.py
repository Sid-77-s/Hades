import os
import json
from pydantic import BaseModel, Field
from typing import Optional

CONFIG_FILE = "config.json"

class APICredentials(BaseModel):
    gemini_key: Optional[str] = None
    openai_key: Optional[str] = None
    gamma_email: Optional[str] = None
    gamma_password: Optional[str] = None

class AppSettings(BaseModel):
    model_provider: str = "gemini"
    allow_background_execution: bool = True
    notifications_level: str = "BETTER_IDEA" # SILENT, BETTER_IDEA, BLOCKER, MEANINGFUL_DECISION, COMPLETE

class HadesConfig(BaseModel):
    api_credentials: APICredentials = Field(default_factory=APICredentials)
    settings: AppSettings = Field(default_factory=AppSettings)

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
        
    def _load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.config = HadesConfig(**data)
            except Exception as e:
                print(f"[ConfigManager] Error loading config: {e}")
                self.config = HadesConfig()
        else:
            self.config = HadesConfig()
            
        if os.getenv("GEMINI_API_KEY") and not self.config.api_credentials.gemini_key:
            self.config.api_credentials.gemini_key = os.getenv("GEMINI_API_KEY").strip().strip('"').strip("'")
            
        if os.getenv("GAMMA_EMAIL") and not self.config.api_credentials.gamma_email:
            self.config.api_credentials.gamma_email = os.getenv("GAMMA_EMAIL")
            self.config.api_credentials.gamma_password = os.getenv("GAMMA_PASSWORD")
            
    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            f.write(self.config.json(indent=2))

    def get_credentials(self) -> APICredentials:
        return self.config.api_credentials

    def get_settings(self) -> AppSettings:
        return self.config.settings
