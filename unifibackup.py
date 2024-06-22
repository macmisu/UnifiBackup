import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options

# Load environment variables
username = os.getenv('uname')
password = os.getenv('passwd')
unifiip = os.getenv('unifiip')

options = Options()
options.add_argument("--allow-running-insecure-content")
options.add_argument("--headless")
# Web Driver for Firefox
driver = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
driver.maximize_window()

# Get Linkedin login page
driver.get(f"https://{unifiip}")

time.sleep(3)

username_field = driver.find_element(By.ID, 'login-username')
username_field.send_keys(f'{username}')
password_field = driver.find_element(By.ID, 'login-password')
password_field.send_keys(f'{password}')
time.sleep(1)
password_field.submit()
time.sleep(2)
console_settings = driver.find_element(By.CSS_SELECTOR, '[data-testid="console-settings"]')
console_settings.click()
time.sleep(1)
backup_button = driver.find_element(By.XPATH, '//span[contains(@class, "content__jTNy2Cxe") and text()="Back Up Now"]')
backup_button.click()

time.sleep(10)
print("backup completed successfully")

time.sleep(100)
driver.quit()
