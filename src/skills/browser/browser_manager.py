from playwright.async_api import async_playwright, Browser, Page, Playwright
from typing import Optional

class BrowserSessionManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BrowserSessionManager, cls).__new__(cls)
            cls._instance.playwright: Optional[Playwright] = None
            cls._instance.browser: Optional[Browser] = None
            cls._instance.page: Optional[Page] = None
            cls._instance.status = "NOT_CONNECTED"
        return cls._instance

    async def get_page(self) -> Page:
        if self.status != "READY" or not self.page:
            await self.start()
        return self.page

    async def start(self):
        if self.status == "READY":
            return
            
        self.status = "STARTING"
        try:
            self.playwright = await async_playwright().start()
            # Defaulting to chromium, headless for autonomous execution
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.page = await self.browser.new_page()
            self.status = "READY"
        except Exception as e:
            self.status = "FAILED"
            print(f"[BrowserSessionManager] Failed to start browser: {e}")
            raise e

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.status = "CLOSED"
        
browser_manager = BrowserSessionManager()
