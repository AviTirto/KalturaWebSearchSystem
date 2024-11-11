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
        # Set Chrome options to specify the download directory
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless=new")

        # Define the download directory
        self.download_dir = os.getenv('SRT_PATH')

        # Create the directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        self.prefs = {"download.default_directory": self.download_dir}
        self.options.add_experimental_option("prefs", self.prefs)

        self.driver = webdriver.Chrome(options=self.options)
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

    def populate_df(self, url):

        # Initialize a list to store scraped data
        data = []

        # Find all divs with the class 'row'
        rows = self.driver.find_elements(By.CLASS_NAME, 'row')

        # Loop through each row
        for row in rows:
        # Find all columns within the row
            cols = row.find_elements(By.CLASS_NAME, 'col-md-4')
            for col in cols:
                # Find all links in the column
                if 'Watch' in col.text:
                    links = col.find_elements(By.TAG_NAME, 'a')
                    for link in links:
                        # Extract the href attribute
                        lecture_link = link.get_attribute('href')
                        
                        # Check if the link contains 'kaltura'
                        if 'mediaspace' in lecture_link:
                            lecture_title = col.find_element(By.TAG_NAME, 'span').text
                            date = col.find_element(By.TAG_NAME, 'strong').text
                            # Store the extracted data
                            data.append({
                                'Date': date,
                                'Title': lecture_title,
                                'Link': lecture_link
                            })

        # Create a DataFrame from the list of data
        self.df = pd.DataFrame(data)

        # Close the driver
        self.driver.quit()

    def execute(self):
        self.populate_df(self.url)
        self.df.to_json('output.json', orient='records', lines=True)

        for url in self.df["Link"]:
            print(url)
            self.download_media(url)
        
        return self.download_dir




