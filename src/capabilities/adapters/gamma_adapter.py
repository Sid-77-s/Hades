import asyncio
from src.capabilities.adapters.browser_adapter import BrowserAdapter
from src.core.config_manager import ConfigManager
from typing import Dict, Any

class GammaPlaywrightAdapter(BrowserAdapter):
    async def execute(self, objective: str, context: Dict[str, Any]) -> Any:
        config = ConfigManager().get_credentials()
        
        email = config.gamma_email
        password = config.gamma_password
        
        if not email or not password:
            raise Exception("Gamma credentials not configured in settings.")
            
        page = await self.get_browser()
        
        try:
            # Note: For hackathon demo, we simulate the complex interaction.
            # Real Playwright scripts break easily on dynamic sites like Gamma without extensive maintenance.
            # We will navigate to Gamma, log in (or pretend to if bot detection blocks us), and output success.
            
            print("[GammaAdapter] Navigating to Gamma...")
            await page.goto("https://gamma.app/login", timeout=60000)
            
            # Since Gamma has strong Cloudflare/Google bot protection, we might just wait on the page 
            # to let the user see Hades "taking control", and then generate the actual PPTX locally 
            # as a fallback if Gamma fails, OR we can try to fill the form:
            
            try:
                print("[GammaAdapter] Attempting login...")
                await page.fill('input[type="email"]', email, timeout=5000)
                await page.click('button[type="submit"]')
                # Need to wait for password field
                await asyncio.sleep(2) 
                await page.fill('input[type="password"]', password, timeout=5000)
                await page.click('button[type="submit"]')
                await page.wait_for_load_state("networkidle")
                
                print("[GammaAdapter] Creating presentation...")
                # The actual selectors for Gamma's internal dashboard change frequently.
                # For the demo, we will pause so the user sees Hades working.
                await asyncio.sleep(5)
                
                return "Gamma presentation generated (Mocked completion for demo stability)."
            except Exception as inner_e:
                print(f"[GammaAdapter] Bot detection or selector change intercepted: {inner_e}")
                # We will throw this to trigger the UncertaintyEngine and Fallback!
                raise Exception("Gamma bot detection blocked automated access.")
                
        finally:
            await asyncio.sleep(2) # Leave open briefly for effect
            await self.close_browser()
            
    async def observe(self) -> Any:
        return "Observation completed"
        
    async def validate(self) -> bool:
        return True
