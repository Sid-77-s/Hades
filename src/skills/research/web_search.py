import httpx
from typing import Any, Dict
from src.skills.base import BaseSkill, SkillMetadata, SkillStatus
from src.core.config_manager import ConfigManager

class WebSearchSkill(BaseSkill):
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            skill_id="web_search",
            name="Web Search",
            description="Searches the web for real-time information.",
            category="research",
            input_schema={
                "query": "Search query string"
            },
            output_schema={
                "results": "List of search results (title, url, snippet)"
            },
            required_credentials=["SEARCH_API_KEY"],
            risk_level="READ"
        )
        
    def verify_health(self) -> tuple[bool, str, str]:
        creds = ConfigManager().get_credentials()
        if creds.search_api_key:
            return True, "Ready", SkillStatus.READY
        return False, "SEARCH_API_KEY missing", SkillStatus.CONFIGURATION_REQUIRED

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        query = params.get("query")
        if not query:
            raise ValueError("query is required")
            
        api_key = ConfigManager().get_credentials().search_api_key
        
        # Example implementation using Tavily API structure
        url = "https://api.tavily.com/search"
        headers = {"Content-Type": "application/json"}
        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "include_answer": False
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
        results = [{"title": r.get("title"), "url": r.get("url"), "snippet": r.get("content")} for r in data.get("results", [])]
        return {"results": results}
