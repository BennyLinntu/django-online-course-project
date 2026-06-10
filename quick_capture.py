#!/usr/bin/env python
"""
Capture real browser screenshots using Playwright
"""
import asyncio
from pathlib import Path

async def main():
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()
        
        # Navigate to admin
        print("Loading admin page...")
        await page.goto('http://127.0.0.1:7777/admin/')
        await page.wait_for_load_state('networkidle')
        
        # Take screenshot
        print("Capturing screenshot...")
        await page.screenshot(path='03-admin-site.png', full_page=True)
        print("✓ Screenshot saved: 03-admin-site.png")
        
        # Verify file exists
        if Path('03-admin-site.png').exists():
            size = Path('03-admin-site.png').stat().st_size
            print(f"  File size: {size:,} bytes")
        
        await browser.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
