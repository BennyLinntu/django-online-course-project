#!/usr/bin/env python
"""
Capture real browser screenshots using Selenium
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def capture_admin_screenshot():
    """Capture Task 3 admin screenshot"""
    print("Capturing Task 3 admin screenshot...")
    
    # Initialize Chrome WebDriver with automatic driver management
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Navigate to admin
        driver.get('http://127.0.0.1:7777/admin/login/?next=/admin/')
        driver.set_window_size(1280, 800)
        
        # Wait for page to load
        time.sleep(2)
        
        # Login
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.send_keys('admin')
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys('admin123')
        
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]")
        login_button.click()
        
        # Wait for admin page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "site-header"))
        )
        time.sleep(2)
        
        # Take screenshot
        driver.save_screenshot('03-admin-site.png')
        print("✓ Saved 03-admin-site.png")
        
    finally:
        driver.quit()

def capture_exam_result_screenshot():
    """Capture Task 7 exam result screenshot"""
    print("Capturing Task 7 exam result screenshot...")
    
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Logout if needed
        driver.get('http://127.0.0.1:7777/logout/')
        time.sleep(1)
        
        # Navigate to login
        driver.get('http://127.0.0.1:7777/login/')
        driver.set_window_size(1280, 800)
        time.sleep(2)
        
        # Login as testuser
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.send_keys('testuser')
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys('testpass123')
        
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()
        
        # Wait for course details page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        time.sleep(2)
        
        # Click first radio button (correct answer)
        radio_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
        if radio_buttons:
            radio_buttons[0].click()
        
        # Submit exam
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit Exam')]")
        submit_button.click()
        
        # Wait for results page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        time.sleep(2)
        
        # Take screenshot
        driver.save_screenshot('07-final.png')
        print("✓ Saved 07-final.png")
        
    finally:
        driver.quit()

if __name__ == '__main__':
    try:
        capture_admin_screenshot()
        capture_exam_result_screenshot()
        print("\nBoth screenshots captured successfully!")
    except Exception as e:
        print(f"Error: {e}")
