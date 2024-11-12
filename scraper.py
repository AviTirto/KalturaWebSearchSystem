from selenium import webdriver
from selenium.webdriver.common.by import By
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

    # This function 
    def populate_df(self, url):
        data = []
        rows = self.driver.find_elements(By.CLASS_NAME, 'row')
        for row in rows:
            cols = row.find_elements(By.CLASS_NAME, 'col-md-4')
            for col in cols:
                if 'Watch' in col.text:
                    links = col.find_elements(By.TAG_NAME, 'a')
                    for link in links:
                        lecture_link = link.get_attribute('href')
                        if 'mediaspace' in lecture_link:
                            lecture_title = col.find_element(By.TAG_NAME, 'span').text
                            date = col.find_element(By.TAG_NAME, 'strong').text
                            embed_link = self.get_embed_link(lecture_link)
                            data.append({'Date': date, 'Title': lecture_title, 'Link': lecture_link, 'embed_link': embed_link})

        self.df = pd.DataFrame(data)
        self.driver.quit()

    def execute(self):
        self.populate_df(self.url)
        self.df.to_json('output.json', orient='records', lines=True)
        for url in self.df["Link"]:
            print(url)
            self.download_media(url)
        return self.download_dir

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
