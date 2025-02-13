from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time
import os
from dotenv import load_dotenv

load_dotenv()

def get_driver():
    """Initializes and returns a Firefox WebDriver with required options."""
    options = webdriver.FirefoxOptions()

    # Download directory
    download_dir = os.getenv('SRT_PATH')
    os.makedirs(download_dir, exist_ok=True)

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", download_dir)
    profile.set_preference("browser.download.useDownloadDir", True)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain,application/octet-stream,application/x-subrip")
    options.profile = profile

    return webdriver.Firefox(options=options), download_dir


def xpath_safe_click(driver, xpath):
    """Clicks an element safely, retrying if necessary."""
    for _ in range(3):
        try:
            element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
            return
        except (StaleElementReferenceException, TimeoutError):
            pass


def get_srt_file(driver, download_dir):
    """Downloads the SRT file and waits for it to appear."""
    xpath_safe_click(driver, '//*[@id="player-gui"]/div[3]/div[1]/div[3]/button')
    
    try:
        xpath_safe_click(driver, '//*[@id="player-gui"]/div[3]/div[2]/div[3]/div/div[3]/div/div/button')
    except:
        return None

    xpath_safe_click(driver, '//*[@id="player-gui"]/div[3]/div[1]/div[1]/div/div/div/div/div/div/div/div[2]')

    # Wait for the file to appear in the download folder
    start_time = time.time()
    timeout = 30

    while time.time() - start_time < timeout:
        files = [f for f in os.listdir(download_dir) if f.endswith('.srt')]
        if files:
            return max(files, key=lambda f: os.path.getmtime(os.path.join(download_dir, f)))

    return None


def get_date(driver):
    """Extracts the date from the lecture page."""
    date_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "js-entry-create-at"))
    ).find_element(By.TAG_NAME, "span")
    return date_element.text


def get_embed_link(driver):
    """Extracts the embed link from the lecture page."""
    xpath_safe_click(driver, '/html/body/div/div[2]/div[5]/div/div[2]/div[4]/div[1]/div/div[1]/ul/li[2]/a/span')
    xpath_safe_click(driver, "/html/body/div/div[2]/div[5]/div/div[2]/div[4]/div[3]/div/div[2]/div/div/div[1]/ul/li[2]")

    embed_text_area = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="embedTextArea"]'))
    )
    return embed_text_area.get_attribute("value")


def scrape_lecture_page(url):
    """Main function to scrape the lecture page and return metadata."""
    driver, download_dir = get_driver()
    try:
        driver.get(url)

        srt_file = get_srt_file(driver, download_dir)
        if not srt_file:
            return None

        return {
            "file_name": os.path.join(download_dir, srt_file),
            "date": get_date(driver),
            "embed_link": get_embed_link(driver),
        }
    finally:
        driver.quit()


def get_lessons(url):
    """Extracts all lessons and their embed links from the playlist page."""
    driver, _ = get_driver()
    lecture_metadata = []

    try:
        driver.get(url)
        lessons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="playlist_item"]'))
        )

        for lesson in lessons:
            title = lesson.get_attribute("title")
            lesson.click()

            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[5]/div/div[2]/div/div[2]/div/div[3]/div/div[1]/div/div[1]/ul/li[2]/a'))
                ).click()

                lecture_link_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[5]/div/div[2]/div/div[2]/div/div[3]/div/div[3]/div/div[2]/div/div/div[2]/div[1]/input'))
                )
                lecture_link = lecture_link_element.get_attribute("value")
            except Exception as e:
                lecture_link = f"Error retrieving link: {e}"

            lecture_metadata.append({'title': title, 'lecture_link': lecture_link})

        return lecture_metadata
    finally:
        driver.quit()
