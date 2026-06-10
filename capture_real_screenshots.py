import asyncio
from playwright.async_api import async_playwright
import time


async def capture_screenshots():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        # Set viewport to a common size
        await page.set_viewport_size({"width": 1280, "height": 720})

        # Task 3 - Admin screenshot
        print("Capturing Task 3 screenshot...")
        await page.goto('http://127.0.0.1:7777/admin/login/?next=/admin/')

        # Wait for page to load
        await page.wait_for_load_state('networkidle')

        # Login
        await page.fill('input[name="username"]', 'admin')
        await page.fill('input[name="password"]', 'admin123')
        await page.click('button:has-text("Log in")')

        # Wait for admin page to load
        await page.wait_for_load_state('networkidle')
        time.sleep(1)

        # Take screenshot
        await page.screenshot(path='03-admin-site.png', full_page=True)
        print("✓ Saved 03-admin-site.png")

        # Task 7 - Exam result screenshot
        print("Capturing Task 7 screenshot...")

        # Logout and login as testuser
        await page.goto('http://127.0.0.1:7777/logout/')
        await page.wait_for_load_state('networkidle')

        # Navigate to login
        await page.goto('http://127.0.0.1:7777/login/')
        await page.wait_for_load_state('networkidle')

        # Login as testuser
        await page.fill('input[name="username"]', 'testuser')
        await page.fill('input[name="password"]', 'testpass123')
        await page.click('button:has-text("Login")')

        # Wait for course details page
        await page.wait_for_load_state('networkidle')
        time.sleep(1)

        # Find and select the correct answer
        # Looking for "A programming language" option
        radios = await page.locator('input[type="radio"]').all()
        if len(radios) > 0:
            # Click the first radio button (which should be "A programming language")
            await radios[0].click()

        # Click submit button
        await page.click('button:has-text("Submit Exam")')

        # Wait for results page
        await page.wait_for_load_state('networkidle')
        time.sleep(1)

        # Take screenshot of results page
        await page.screenshot(path='07-final.png', full_page=True)
        print("✓ Saved 07-final.png")

        await browser.close()
        print("\nBoth screenshots captured successfully!")

if __name__ == '__main__':
    asyncio.run(capture_screenshots())
