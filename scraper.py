from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def download_media(url):
    # Define the download directory
    download_dir = os.getenv('SRT_PATH')

    # Create the directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Set Chrome options to specify the download directory
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_dir}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        time.sleep(7)

        play_button = driver.find_element(By.XPATH, '//*[@id="player-gui"]/div[3]/div[1]/div[3]/button')
        play_button.click()

        time.sleep(2)

        download_button = driver.find_element(By.XPATH, '//*[@id="player-gui"]/div[3]/div[2]/div[3]/div/div[3]/div/div/button')
        download_button.click()

        time.sleep(10)

        final_button = driver.find_element(By.XPATH, '//*[@id="player-gui"]/div[3]/div[1]/div[1]/div/div/div/div/div[2]/div/div/div/div[3]/div')
        final_button.click()

        time.sleep(10)

    finally:
        driver.quit()

def populate_df(url):
    # Initialize the Chrome driver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Initialize a list to store scraped data
    data = []

    # Find all divs with the class 'row'
    rows = driver.find_elements(By.CLASS_NAME, 'row')

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
    df = pd.DataFrame(data)

    # Close the driver
    driver.quit()
    return df

# Example usage
url = "https://tyler.caraza-harter.com/cs544/f24/schedule.html"  # Replace with your desired URL
df = populate_df(url)
df.to_json('output.json', orient='records', lines=True)


## RUN THE FOLLOWING WHEN YOU WANT TO DOWNLOAD THE SRT FILES
#for url in df["Link"]:
    #print(url)
    #download_media(url)
