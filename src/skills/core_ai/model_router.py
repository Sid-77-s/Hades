from typing import Any, Dict, List
from src.skills.base import BaseSkill, SkillMetadata, SkillStatus
from src.core.config_manager import ConfigManager
import litellm

class ModelRouterSkill(BaseSkill):
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            skill_id="model_router",
            name="Model Router",
            description="Routes requests to the optimal AI model based on configuration and availability.",
            category="core_ai",
            input_schema={
                "messages": "List of message dicts",
                "temperature": "Optional float"
            },
            output_schema={
                "content": "String response from the model"
            },
            required_credentials=["GEMINI_API_KEY", "OPENAI_API_KEY"],
            risk_level="READ",
            supported_providers=["gemini", "openai"]
        )
        
    def verify_health(self) -> tuple[bool, str, str]:
        creds = ConfigManager().get_credentials()
        has_gemini = bool(creds.gemini_key)
        has_openai = bool(creds.openai_key)
        
        if has_gemini or has_openai:
            return True, "Providers available", SkillStatus.READY
        return False, "No valid API keys found", SkillStatus.CONFIGURATION_REQUIRED

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        messages = params.get("messages", [])
        temperature = params.get("temperature", 0.7)
        
        creds = ConfigManager().get_credentials()
        
        # Primary routing logic
        if creds.gemini_key:
            model = "gemini/gemini-1.5-pro-latest"
            litellm.api_key = creds.gemini_key
        elif creds.openai_key:
            model = "openai/gpt-4o"
            litellm.api_key = creds.openai_key
        else:
            raise ValueError("No configured AI providers available for routing.")
            
        response = await litellm.acompletion(
            model=model,
            messages=messages,
            temperature=temperature
        )
        
        return {"content": response.choices[0].message.content}
