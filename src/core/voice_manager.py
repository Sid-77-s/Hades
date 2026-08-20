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

    def get_audio_base64(self, text: str) -> str:
        """
        Generates TTS audio using Kokoro-ONNX and returns it as a base64 data URI.
        """
        if not self.enabled:
            return ""

        import os
        import time
        import base64
        import soundfile as sf
        from kokoro_onnx import Kokoro
        import urllib.request
        import numpy as np

        model_dir = "models"
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, "kokoro-v1.0.onnx")
        voices_path = os.path.join(model_dir, "voices-v1.0.bin")

        if not os.path.exists(model_path):
            print("[VoiceManager] Downloading Kokoro ONNX model (this may take a minute)...")
            urllib.request.urlretrieve("https://github.com/thewh1teagle/kokoro-onnx/releases/download/model/kokoro-v1.0.onnx", model_path)
        if not os.path.exists(voices_path):
            print("[VoiceManager] Downloading Kokoro voices...")
            urllib.request.urlretrieve("https://github.com/thewh1teagle/kokoro-onnx/releases/download/model/voices-v1.0.bin", voices_path)

        try:
            # We initialize Kokoro instance lazily
            if not hasattr(self, "_kokoro"):
                self._kokoro = Kokoro(model_path, voices_path)
            
            # Use af_sky as a calm, intelligent female voice (or am_adam for male)
            voice_name = "af_sky" 
            if self.voice_id == "en_us_1":
                voice_name = "am_adam"
                
            samples, sample_rate = self._kokoro.create(
                text, voice=voice_name, speed=1.0, lang="en-us"
            )
            
            os.makedirs("static/audio", exist_ok=True)
            filename = f"static/audio/{int(time.time()*1000)}.wav"
            
            sf.write(filename, samples, sample_rate)
            
            with open(filename, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                
            # Clean up the file to avoid disk bloat
            os.remove(filename)
            
            return f"data:audio/wav;base64,{encoded}"
        except Exception as e:
            print(f"[VoiceManager] TTS Error: {e}")
            return ""

voice_manager = VoiceManager()
