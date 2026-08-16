import os
import threading
from typing import Dict, Any, List

class VoiceManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(VoiceManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.enabled = True
        self.rate = 180  # Speed (words per minute)
        self.volume = 0.9  # Volume (0.0 to 1.0)
        self.voice_id = None
        self.available_voices: List[Dict[str, str]] = [
            {"id": "en_us_1", "name": "English (US) - Natural Male", "languages": ["en"]},
            {"id": "en_uk_1", "name": "English (UK) - Natural Partner", "languages": ["en"]}
        ]
        self._initialized = True

    def get_settings(self) -> Dict[str, Any]:
        return {
            "enabled": self.enabled,
            "rate": self.rate,
            "volume": self.volume,
            "voice_id": self.voice_id,
            "available_voices": self.available_voices
        }

    def update_settings(self, settings: Dict[str, Any]):
        if "enabled" in settings:
            self.enabled = bool(settings["enabled"])
        if "rate" in settings:
            self.rate = int(settings["rate"])
        if "volume" in settings:
            self.volume = float(settings["volume"])
        if "voice_id" in settings and settings["voice_id"]:
            self.voice_id = str(settings["voice_id"])

    def speak(self, text: str):
        # Frontend handles high-quality speech synthesis directly in browser to prevent Python COM thread blocks
        pass

voice_manager = VoiceManager()
