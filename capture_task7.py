#!/usr/bin/env python
"""
Capture Task 7 - Exam result screenshot using Playwright
"""
import asyncio
from pathlib import Path

async def main():
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()
        
        try:
            # Navigate to login
            print("Loading login page...")
            await page.goto('http://127.0.0.1:7777/login/')
            await page.wait_for_load_state('networkidle')
            
            # Login as testuser
            print("Logging in as testuser...")
            await page.fill('input[name="username"]', 'testuser')
            await page.fill('input[name="password"]', 'testpass123')
            await page.click('button:has-text("Login")')
            
            # Wait for course details page
            await page.wait_for_load_state('networkidle')
            
            # Select answer - click the first radio button
            print("Selecting answer...")
            radios = await page.locator('input[type="radio"]').all()
            if radios:
                await radios[0].click()
            
            # Submit exam
            print("Submitting exam...")
            await page.click('button:has-text("Submit Exam")')
            
            # Wait for results page
            await page.wait_for_load_state('networkidle')
            
            # Verify we're on results page
            title = await page.title()
            print(f"Current page title: {title}")
            
            # Take screenshot
            print("Capturing screenshot...")
            await page.screenshot(path='07-final.png', full_page=True)
            print("✓ Screenshot saved: 07-final.png")
            
            # Verify file exists
            if Path('07-final.png').exists():
                size = Path('07-final.png').stat().st_size
                print(f"  File size: {size:,} bytes")
        
        finally:
            await browser.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
