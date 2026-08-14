from src.capabilities.registry import BaseAdapter
from typing import Dict, Any

class BrowserAdapter(BaseAdapter):
    def __init__(self):
        # We will import playwright locally to avoid loading it if not needed
        pass
        
    async def get_browser(self):
        from playwright.async_api import async_playwright
        self.playwright = await async_playwright().start()
        # Non-headless for demo visibility!
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        return self.page
        
    async def close_browser(self):
        if hasattr(self, 'browser'):
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
