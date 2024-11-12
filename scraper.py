from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    def download_media(self, url):
        try:
            self.driver.get(url)
            time.sleep(7)

            play_button = self.driver.find_element(By.XPATH, '//*[@id="player-gui"]/div[3]/div[1]/div[3]/button')
            play_button.click()
            time.sleep(2)

            download_button = self.driver.find_element(By.XPATH, '//*[@id="player-gui"]/div[3]/div[2]/div[3]/div/div[3]/div/div/button')
            download_button.click()
            time.sleep(10)

            final_button = self.driver.find_element(By.XPATH, '//*[@id="player-gui"]/div[3]/div[1]/div[1]/div/div/div/div/div[2]/div/div/div/div[3]/div')
            final_button.click()
            time.sleep(10)

        finally:
            self.driver.quit()

    def get_srt_file(self, url):
        try:
            # Navigate to the URL
            self.driver.get(url)

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
            timeout = 20  # Max wait time
            downloaded_file = None

            while time.time() - start_time < timeout:
                # Get a list of .srt files in the download directory
                files = [f for f in os.listdir(self.download_dir) if f.endswith('.srt')]
                
                if files:
                    # Get the most recently modified file
                    newest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(self.download_dir, f)))
                    downloaded_file = newest_file
                    break
                time.sleep(1)

            if downloaded_file:
                return os.path.join(self.download_dir, downloaded_file)
            else:
                raise FileNotFoundError("SRT file download timed out or failed.")

        finally:
            self.driver.quit()
            

    def get_lecture_metadata(self, url):
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
                    'date': lesson.find_element(By.TAG_NAME, 'h5').find_element(By.TAG_NAME, "strong").text,
                    'lecture_link': lesson.find_element(By.CSS_SELECTOR, 'a[href*="https://mediaspace.wisc.edu"]').get_attribute('href')
                }
                for lesson in lessons
            ]
            self.driver.quit()
            return lecture_metadata

        except Exception as e:
            return f'Error: {e}'


    def get_embed_link(self, link):
        try:
            self.driver.get(link)
            time.sleep(2)
            share_button = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/div[5]/div/div[2]/div[4]/div[1]/div/div[1]/ul/li[2]/a/span")
            share_button.click()
            time.sleep(2)
            embed_button = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[5]/div/div[2]/div[4]/div[3]/div/div[2]/div/div/div[1]/ul/li[2]')
            embed_button.click()
            time.sleep(2)
            embed_text_area = self.driver.find_element(By.XPATH, '//*[@id="embedTextArea"]')
            embed_text = embed_text_area.get_attribute("value")
            return embed_text
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.driver.quit()
