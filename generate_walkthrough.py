import asyncio
from playwright.async_api import async_playwright
import os
import shutil

async def run():
    print("Starting Playwright to record walkthrough...")
    async with async_playwright() as p:
        # Launch browser with video recording enabled
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            record_video_dir="output_video/",
            record_video_size={"width": 1280, "height": 720}
        )
        page = await context.new_page()

        print("Navigating to http://localhost:5173 ...")
        await page.goto("http://localhost:5173", timeout=60000)
        
        # Handle INIT screen
        print("Handling INIT screen...")
        try:
            await page.wait_for_selector('input[placeholder="Enter Designation..."]', timeout=10000)
            await page.fill('input[placeholder="Enter Designation..."]', "Alex")
            await page.click('button:has-text("INITIALIZE")')
        except Exception:
            print("Init screen not found, assuming already initialized.")

        # Wait for the main UI
        await page.wait_for_selector('text=HADES', timeout=15000)
        await asyncio.sleep(2)
        
        # 1. Open Settings
        print("Opening Settings...")
        await page.click('button[aria-label="Settings"]')
        await asyncio.sleep(1)
        
        # 2. Click "Test" next to Groq Llama 3.3 70B
        print("Testing Llama 3.3 70B (Groq)...")
        # We need to find the Test button for Groq Llama 3
        test_buttons = await page.query_selector_all('text=Test')
        if test_buttons and len(test_buttons) > 2:
            # Click the 3rd one which is Groq based on our config order
            await test_buttons[2].click()
            await asyncio.sleep(2)
        else:
            print("Could not find Test buttons easily. Proceeding...")

        # 3. Close Settings modal
        print("Closing Settings modal...")
        await page.keyboard.press("Escape")
        await asyncio.sleep(1)
        
        # 4. Type an exploratory query
        print("Submitting exploratory query...")
        await page.fill('input#composer', "Research the current AI operating system landscape, identify the strongest existing approaches, understand the major gaps, and tell me where Hades could genuinely differentiate.")
        await page.keyboard.press("Enter")
        
        # Wait for response and background work
        print("Waiting for response and background execution (70s)...")
        await asyncio.sleep(70)
        
        # 5. Scroll up to demonstrate scrolling fix
        print("Scrolling up...")
        await page.mouse.wheel(0, -500)
        await asyncio.sleep(5)
        
        print("Scrolling back down...")
        await page.mouse.wheel(0, 500)
        await asyncio.sleep(5)
        
        await context.close()
        await browser.close()
        
        print("Walkthrough recording complete.")
        
        # Find the webm file and rename it
        for file in os.listdir("output_video"):
            if file.endswith(".webm"):
                shutil.move(os.path.join("output_video", file), "walkthrough.webm")
                break
                
        print("Saved to walkthrough.webm")

if __name__ == "__main__":
    asyncio.run(run())
