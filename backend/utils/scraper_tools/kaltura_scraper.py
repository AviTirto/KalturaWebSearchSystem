from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time
import os
from dotenv import load_dotenv
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

load_dotenv()

def initialize_driver():
    options = Options()
    
    # Get the absolute path for downloads
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
    download_dir = os.path.join(project_root, 'lecture_srt')
    
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        
    print(f"Download directory: {download_dir}")

    # Set Firefox preferences
    options.set_preference('browser.download.folderList', 2)
    options.set_preference('browser.download.manager.showWhenStarting', False)
    options.set_preference('browser.download.dir', download_dir)
    options.set_preference('browser.helperApps.neverAsk.saveToDisk', 
        'application/x-subrip;text/srt;text/plain;application/octet-stream;application/binary')
    options.set_preference('browser.download.manager.showAlertOnComplete', False)
    options.set_preference('browser.download.manager.closeWhenDone', True)
    options.set_preference('pdfjs.disabled', True)  # Disable PDF viewer

    # Create and return the driver
    driver = webdriver.Firefox(options=options)
    return driver, download_dir

def xpath_safe_click(driver, xpath):
    attempts = 3
    for _ in range(attempts):
        try:
            element = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            return
        except (StaleElementReferenceException, TimeoutError):
            pass

def get_srt_file(driver, download_dir):
    xpath_safe_click(driver, '//*[@id="player-gui"]/div[3]/div[1]/div[3]/button')
    try:
        xpath_safe_click(driver, '//*[@id="player-gui"]/div[3]/div[2]/div[3]/div/div[3]/div/div/button')
    except:
        return None
    xpath_safe_click(driver, '//*[@id="player-gui"]/div[3]/div[1]/div[1]/div/div/div/div/div/div/div/div[2]')
    
    start_time = time.time()
    timeout = 30
    while time.time() - start_time < timeout:
        files = [f for f in os.listdir(download_dir) if f.endswith('.srt')]
        if files:
            return max(files, key=lambda f: os.path.getmtime(os.path.join(download_dir, f)))
    return None

def get_date(driver):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "js-entry-create-at"))
    ).find_element(By.TAG_NAME, "span").text

def get_embed_link(driver):
    xpath_safe_click(driver, '/html/body/div/div[2]/div[5]/div/div[2]/div[4]/div[1]/div/div[1]/ul/li[2]/a/span')
    xpath_safe_click(driver, "/html/body/div/div[2]/div[5]/div/div[2]/div[4]/div[3]/div/div[2]/div/div/div[1]/ul/li[2]")
    embed_text_area = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="embedTextArea"]'))
    )
    return embed_text_area.get_attribute("value")

def scrape_lecture_page(driver, url, download_dir):
    driver.get(url)
    downloaded_file = get_srt_file(driver, download_dir)
    if not downloaded_file:
        return None
    date = get_date(driver)
    embed_link = get_embed_link(driver)
    return {
        "file_name": os.path.join(download_dir, downloaded_file),
        "date": date,
        "embed_link": embed_link
    }

def get_lessons(driver, url):
    driver.get(url)
    lecture_metadata = []
    try:
        lessons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="playlist_item"]'))
        )
        for lesson in lessons:
            title = lesson.get_attribute("title")
            try:
                lesson.click()
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[5]/div/div[2]/div/div[2]/div/div[3]/div/div[1]/div/div[1]/ul/li[2]/a'))
                ).click()
                lecture_link_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[5]/div/div[2]/div/div[2]/div/div[3]/div/div[3]/div/div[2]/div/div/div[2]/div[1]/input'))
                )
                lecture_link = lecture_link_element.get_attribute("value")
            except Exception as e:
                lecture_link = f"Error retrieving link: {e}"
            lecture_metadata.append({
                'title': title,
                'lecture_link': lecture_link
            })
        return lecture_metadata
    except Exception as e:
        return f'Error: {e}'
