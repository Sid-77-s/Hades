import re
import httpx
from typing import Any, Dict
from src.skills.base import BaseSkill, SkillMetadata, SkillStatus
from src.skills.browser.browser_manager import browser_manager

class BrowserNavigateSkill(BaseSkill):
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            skill_id="browser_navigate",
            name="Browser Navigation & Web Scraper",
            description="Navigates to a specific URL and returns the page content, text, or title.",
            category="browser",
            input_schema={
                "url": "The URL to navigate to"
            },
            output_schema={
                "title": "Page title",
                "content": "Page content summary or raw text",
                "url": "Resolved URL"
            },
            risk_level="READ",
            supported_providers=["playwright", "http_scraper"]
        )
        
    def verify_health(self) -> tuple[bool, str, str]:
        if browser_manager.is_available():
            return True, "Playwright available", SkillStatus.READY
        return True, "HTTP Web Engine available (Fallback)", SkillStatus.PARTIAL

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        url = params.get("url")
        if not url:
            raise ValueError("url is required")
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        if browser_manager.is_available():
            try:
                page = await browser_manager.get_page()
                await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                title = await page.title()
                content = await page.evaluate("document.body.innerText")
                if len(content) > 5000:
                    content = content[:5000] + "... [truncated]"
                return {
                    "title": title,
                    "content": content,
                    "url": url,
                    "engine": "playwright"
                }
            except Exception as e:
                print(f"[BrowserNavigateSkill] Playwright navigation failed: {e}. Falling back to HTTP...")

        # Fallback to httpx
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
                resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Hades/1.0"})
                html = resp.text
                title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
                title = title_match.group(1).strip() if title_match else url
                # Strip HTML tags
                text = re.sub(r"<[^>]+>", " ", html)
                text = re.sub(r"\s+", " ", text).strip()
                if len(text) > 5000:
                    text = text[:5000] + "... [truncated]"
                return {
                    "title": title,
                    "content": text,
                    "url": str(resp.url),
                    "engine": "http_scraper"
                }
        except Exception as e:
            return {"error": f"Failed to load URL {url}: {e}", "url": url}

