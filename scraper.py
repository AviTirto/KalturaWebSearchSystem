from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def download_media(url):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        time.sleep(5)

        play_button = driver.find_element(By.XPATH, '//*[@id="player-gui"]/div[3]/div[1]/div[3]/button/div/i')
        play_button.click()

        time.sleep(2)

        download_button = driver.find_element(By.XPATH, '//*[@id="player-gui"]/div[3]/div[2]/div[3]/div/div[1]/div/div/button/i')
        download_button.click()

        time.sleep(10)

        final_button = driver.find_element(By.XPATH, '//*[@id="player-gui"]/div[3]/div[1]/div[1]/div/div/div/div/div[2]/div/div/div/div[3]')
        final_button.click()

        time.sleep(10)

    finally:
        driver.quit()

def get_page_html(url):
    # Set up Chrome options (you can customize as needed)
    options = webdriver.ChromeOptions()
    
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=options)

    try:
        # Open the specified URL
        driver.get(url)

        # Get the entire HTML content of the page
        html_content = driver.page_source

        return html_content

    finally:
        # Close the browser
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
            # Check if 'Watch' exists in the column
            if 'Watch' in col.text:
                # Extract the link and other relevant data
                lecture_link = col.find_element(By.TAG_NAME, 'a').get_attribute('href')
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
print(df)  # Print the HTML content or process it as needed
