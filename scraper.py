from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

class Scraper():
    def __init__(self):
        self.df = None
        # Set Firefox options
        self.options = webdriver.FirefoxOptions()
        #self.options.add_argument("--headless")  # headless mode if needed

        # Define the download directory
        self.download_dir = os.getenv('SRT_PATH')

        # Create the directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        # Set up the Firefox profile
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("browser.download.folderList", 2)  # 2 means custom location
        self.profile.set_preference("browser.download.dir", self.download_dir)
        self.profile.set_preference("browser.download.useDownloadDir", True)
        self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")  # Specify MIME types as needed
        
        # Add profile to options
        self.options.profile = self.profile

        # Initialize the Firefox driver with options
        self.driver = webdriver.Firefox(options=self.options)
        self.url = "https://tyler.caraza-harter.com/cs544/f24/schedule.html"

    def get_srt_file(self):
        # Wait for play button and click
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="player-gui"]/div[3]/div[1]/div[3]/button'))
        ).click()

        # Wait for download button and click
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="player-gui"]/div[3]/div[2]/div[3]/div/div[3]/div/div/button'))
        ).click()

        # Wait for final button and click
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="player-gui"]/div[3]/div[1]/div[1]/div/div/div/div/div[2]/div/div/div/div[3]/div'))
        ).click()

        # Wait for file to appear in the download folder
        start_time = time.time()
        timeout = 30  # Max wait time
        downloaded_file = None

        while time.time() - start_time < timeout:
            # Get a list of .srt files in the download directory
            files = [f for f in os.listdir(self.download_dir) if f.endswith('.srt')]
                
            if files:
                # Get the most recently modified file
                newest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(self.download_dir, f)))
                downloaded_file = newest_file
                break

        return downloaded_file
        
    def get_date(self):
        # Retry loop for getting the date text
        max_attempts = 3
        date = None

        for attempt in range(max_attempts):
            try:
                # Locate and retrieve the text of the date
                date = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "js-entry-create-at"))
                ).find_element(By.TAG_NAME, "span").text
                break  # Exit loop if successful
            except StaleElementReferenceException:
                # If a stale reference occurs, wait briefly and retry
                if attempt < max_attempts - 1:
                    time.sleep(1)  # Wait 1 second before retrying
                else:
                    raise  # Raise the exception if all attempts fail

        return date


    def scrape_lecture_page(self, url):
        try:
            # Navigate to the URL
            self.driver.get(url)

            downloaded_file = self.get_srt_file()

            date = self.get_date()

            embed_link = self.get_embed_link()

            # Return result if date and downloaded file are successfully retrieved
            if downloaded_file:
                return {
                    "file_name": os.path.join(self.download_dir, downloaded_file),
                    "date": date,
                    'embed_link': embed_link
                }
            else:
                raise FileNotFoundError("SRT file download timed out or failed.")

        finally:
            pass
            # self.driver.quit()


    def get_lessons(self, url):
        lecture_metadata = []
        try:
            # grab all lessons
            self.driver.get(url)
            lessons = self.driver.find_elements(By.CSS_SELECTOR, 'div.col-md-4')
            
            # filter for the ones with a kaltura lecture
            lessons = [lesson for lesson in lessons if lesson.find_elements(By.CSS_SELECTOR, 'a[href*="https://mediaspace.wisc.edu"]')]

            lecture_metadata = [
                {
                    'title': lesson.find_element(By.TAG_NAME, 'h5').text,
                    'lecture_link': lesson.find_element(By.CSS_SELECTOR, 'a[href*="https://mediaspace.wisc.edu"]').get_attribute('href')
                }
                for lesson in lessons
            ]
            # self.driver.quit()
            return lecture_metadata

        except Exception as e:
            return f'Error: {e}'


    def get_embed_link(self):
        """Retrieves the embed link from the page with retries."""
        retries = 3
        for attempt in range(retries):
            try:

                # Wait for the share button and click
                share_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[5]/div/div[2]/div[4]/div[1]/div/div[1]/ul/li[2]/a/span"))
                )
                share_button.click()

                # Wait for the embed button and click
                embed_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div[5]/div/div[2]/div[4]/div[3]/div/div[2]/div/div/div[1]/ul/li[2]'))
                )
                embed_button.click()

                # Wait for the embed text area to be present
                embed_text_area = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="embedTextArea"]'))
                )
                embed_text = embed_text_area.get_attribute("value")
                return embed_text

            except Exception as e:
                if attempt < retries - 1:
                    print(f"Attempt {attempt + 1} failed, retrying... Error: {e}")
                    time.sleep(2)  # Wait briefly before retrying
                else:
                    print(f"All attempts failed. Error: {e}")
                    return None
