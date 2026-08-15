from typing import Any, Dict
from src.skills.base import BaseSkill, SkillMetadata, SkillStatus
from src.skills.browser.browser_manager import browser_manager

class BrowserNavigateSkill(BaseSkill):
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            skill_id="browser_navigate",
            name="Browser Navigation",
            description="Navigates to a specific URL and returns the page content or title.",
            category="browser",
            input_schema={
                "url": "The URL to navigate to"
            },
            output_schema={
                "title": "Page title",
                "content": "Page content summary or raw text"
            },
            risk_level="READ"
        )
        
    def verify_health(self) -> tuple[bool, str, str]:
        return True, "Playwright available", SkillStatus.READY

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        url = params.get("url")
        if not url:
            raise ValueError("url is required")
            
        page = await browser_manager.get_page()
        await page.goto(url, wait_until="domcontentloaded")
        
        title = await page.title()
        content = await page.evaluate("document.body.innerText")
        
        # Truncate content for reasoning to avoid blowing up context window
        if len(content) > 5000:
            content = content[:5000] + "... [truncated]"
            
        return {
            "title": title,
            "content": content
        }
