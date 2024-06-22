import os
import logging
import shutil
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_environment_variables():
    username = os.getenv('uname')
    password = os.getenv('passwd')
    unifiip = os.getenv('unifiip')
    backupInterval = int(os.getenv('backupInterval', '24'))  # default to 24 hours if not set
    output_directory = os.getenv('outputDirectory', os.path.expanduser('~/Downloads'))  # default to ~/Downloads if not set
    return username, password, unifiip, backupInterval, output_directory

def sleep_hours(hours):
    seconds = hours * 3600
    interval = 60  # sleep in 1-minute intervals
    while seconds > 0:
        time.sleep(min(interval, seconds))
        seconds -= interval

def setup_webdriver():
    options = Options()
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
    return driver

def login_to_unifi(driver, username, password, unifiip):
    driver.get(f"https://{unifiip}")
    time.sleep(3)
    
    if username:
        username_field = driver.find_element(By.ID, 'login-username')
        logging.info("Username field found, entering username.")
        username_field.send_keys(username)
    
    if password:
        password_field = driver.find_element(By.ID, 'login-password')
        logging.info("Password field found, entering password.")
        password_field.send_keys(password)
        time.sleep(1)
        password_field.submit()
        time.sleep(2)

def perform_backup(driver, output_directory):
    console_settings = driver.find_element(By.CSS_SELECTOR, '[data-testid="console-settings"]')
    logging.info("Found Console Settings.")
    console_settings.click()
    time.sleep(1)
    
    backup_button = driver.find_element(By.XPATH, '//span[contains(@class, "content__jTNy2Cxe") and text()="Back Up Now"]')
    logging.info("Backup field found, backing up now.")
    backup_button.click()
    logging.info("Waiting for backup to download...")
    time.sleep(30)
    
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        logging.info(f"Created output directory: {output_directory}")
    
    # Assume the most recent file in Downloads is the backup file
    downloads_path = os.path.expanduser('~/Downloads')
    latest_file = max([os.path.join(downloads_path, f) for f in os.listdir(downloads_path)], key=os.path.getctime)
    
    current_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    new_file_name = f"unifi_os_backup_{current_time}.unifi"
    new_file_path = os.path.join(output_directory, new_file_name)
    
    shutil.move(latest_file, new_file_path)
    logging.info(f"Backup completed successfully. File saved as {new_file_path}")

def main():
    username, password, unifiip, backupInterval, output_directory = load_environment_variables()
    driver = setup_webdriver()
    
    try:
        while True:
            login_to_unifi(driver, username, password, unifiip)
            perform_backup(driver, output_directory)
            logging.info(f"Sleeping for {backupInterval} hours")
            sleep_hours(backupInterval)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
