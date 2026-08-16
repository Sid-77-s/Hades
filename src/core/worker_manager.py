import os
import json
from typing import List, Dict, Any, Optional
import litellm

CONFIG_FILE = "config.json"

DEFAULT_WORKERS = [
    {
        "id": "gemini-flash",
        "provider": "google",
        "model_name": "gemini/gemini-flash-latest",
        "display_name": "Gemini Flash (Latest)",
        "capabilities": ["general", "fast", "research", "vision"],
        "specialization": "Fast / Research (Free Tier)",
        "enabled": True,
        "env_key": "GEMINI_API_KEY"
    },
    {
        "id": "gemini-3.5",
        "provider": "google",
        "model_name": "gemini/gemini-3.5-flash",
        "display_name": "Gemini 3.5 Flash",
        "capabilities": ["general", "fast", "coding", "research"],
        "specialization": "Coding / Fast (Free Tier)",
        "enabled": True,
        "env_key": "GEMINI_API_KEY"
    },
    {
        "id": "groq-llama3-70b",
        "provider": "groq",
        "model_name": "groq/llama-3.3-70b-versatile",
        "display_name": "Llama 3.3 70B (Groq)",
        "capabilities": ["general", "reasoning", "coding", "fast"],
        "specialization": "Ultra Fast Open-Source (Free Tier)",
        "enabled": True,
        "env_key": "GROQ_API_KEY"
    },
    {
        "id": "groq-mixtral",
        "provider": "groq",
        "model_name": "groq/mixtral-8x7b-32768",
        "display_name": "Mixtral 8x7B (Groq)",
        "capabilities": ["general", "coding", "fast"],
        "specialization": "Open Source Mixture-of-Experts (Free Tier)",
        "enabled": True,
        "env_key": "GROQ_API_KEY"
    },
    {
        "id": "openrouter-free",
        "provider": "openrouter",
        "model_name": "openrouter/meta-llama/llama-3.2-3b-instruct:free",
        "display_name": "Llama 3.2 (OpenRouter Free)",
        "capabilities": ["general", "fast"],
        "specialization": "100% Free Public Endpoint",
        "enabled": True,
        "env_key": "OPENROUTER_API_KEY"
    },
    {
        "id": "ollama-local",
        "provider": "ollama",
        "model_name": "ollama/llama3",
        "display_name": "Llama 3 (Local Ollama)",
        "capabilities": ["general", "coding", "privacy"],
        "specialization": "Local Open Source / 100% Free (No Key Required)",
        "enabled": True,
        "env_key": "OLLAMA_API_BASE"
    },
    {
        "id": "gpt-4o",
        "provider": "openai",
        "model_name": "gpt-4o",
        "display_name": "GPT-4o",
        "capabilities": ["general", "reasoning", "vision", "coding"],
        "specialization": "Reasoning / General",
        "enabled": True,
        "env_key": "OPENAI_API_KEY"
    },
    {
        "id": "claude-3-5-sonnet",
        "provider": "anthropic",
        "model_name": "claude-3-5-sonnet-20241022",
        "display_name": "Claude 3.5 Sonnet",
        "capabilities": ["reasoning", "coding", "research"],
        "specialization": "Coding / Reasoning",
        "enabled": False,
        "env_key": "ANTHROPIC_API_KEY"
    }
]

class WorkerManager:
    def __init__(self):
        self.workers: List[Dict[str, Any]] = []
        self.load_workers()

    def load_workers(self):
        self.workers = DEFAULT_WORKERS
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    custom_workers = data.get("workers", [])
                    if custom_workers:
                        # Merge or update
                        existing_ids = {w["id"] for w in DEFAULT_WORKERS}
                        for cw in custom_workers:
                            if cw["id"] not in existing_ids:
                                self.workers.append(cw)
            except Exception as e:
                print(f"[WorkerManager] Failed to load workers: {e}")
        self.save_workers()

    def save_workers(self):
        data = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
            except Exception:
                pass
        data["workers"] = self.workers
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[WorkerManager] Failed to save workers: {e}")

    def get_workers_status(self) -> List[Dict[str, Any]]:
        result = []
        for w in self.workers:
            # Special check for local Ollama
            if w.get("provider") == "ollama":
                has_key = True  # Ollama runs locally without key
            else:
                has_key = bool(os.getenv(w.get("env_key", ""), ""))
            
            result.append({
                "id": w["id"],
                "provider": w["provider"],
                "model_name": w["model_name"],
                "display_name": w.get("display_name", w["model_name"]),
                "capabilities": w.get("capabilities", ["general"]),
                "specialization": w.get("specialization", "General"),
                "enabled": w.get("enabled", True),
                "available": has_key,
                "configured": has_key
            })
        return result

    def add_worker(self, worker_data: Dict[str, Any]):
        worker_id = worker_data.get("id") or f"worker-{len(self.workers) + 1}"
        worker_data["id"] = worker_id
        self.workers.append(worker_data)
        self.save_workers()
        return worker_data

    def toggle_worker(self, worker_id: str, enabled: bool):
        for w in self.workers:
            if w["id"] == worker_id:
                w["enabled"] = enabled
                self.save_workers()
                return True
        return False

    def remove_worker(self, worker_id: str):
        self.workers = [w for w in self.workers if w["id"] != worker_id]
        self.save_workers()
        return True

    def select_worker(self, required_capability: str = "general") -> Optional[str]:
        """Automatically select the best available and enabled worker for the capability."""
        candidates = []
        for w in self.workers:
            if not w.get("enabled", True):
                continue
            has_key = bool(os.getenv(w.get("env_key", ""), ""))
            if not has_key and w.get("provider") != "ollama":
                continue
            if required_capability in w.get("capabilities", ["general"]) or required_capability == "general":
                candidates.append(w["model_name"])

        if candidates:
            return candidates[0]
        
        for w in self.workers:
            if os.getenv(w.get("env_key", ""), "") or w.get("provider") == "ollama":
                return w["model_name"]
        return "gemini/gemini-flash-latest"

    def test_worker(self, model_name: str) -> Dict[str, Any]:
        try:
            res = litellm.completion(
                model=model_name,
                messages=[{"role": "user", "content": "Ping test"}],
                max_tokens=10
            )
            return {"success": True, "message": "Worker connection verified."}
        except Exception as e:
            return {"success": False, "error": str(e)}

worker_manager = WorkerManager()
