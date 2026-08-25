from typing import Optional, Any

try:
    from playwright.async_api import async_playwright, Browser, Page, Playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Browser = Any
    Page = Any
    Playwright = Any

class BrowserSessionManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BrowserSessionManager, cls).__new__(cls)
            cls._instance.playwright = None
            cls._instance.browser = None
            cls._instance.page = None
            cls._instance.status = "NOT_CONNECTED"
        return cls._instance

    def is_available(self) -> bool:
        return PLAYWRIGHT_AVAILABLE

    async def get_page(self) -> Any:
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("Playwright is not installed. Install with 'pip install playwright && playwright install chromium'")
        if self.status != "READY" or not self.page:
            await self.start()
        return self.page

    async def start(self):
        if not PLAYWRIGHT_AVAILABLE:
            self.status = "UNAVAILABLE"
            return
            
        if self.status == "READY":
            return
            
        self.status = "STARTING"
        try:
            self.playwright = await async_playwright().start()
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

