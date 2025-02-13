import sys
import os
import shutil
import asyncio
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

# Adjust path for project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)

from backend.utils.scraper_tools.kaltura_scraper import *
from backend.utils.parsing_tools.srt_parser import *
from backend.utils.zilliz_tools.zilliz_api import *
from backend.utils.encoders import *
from backend.utils.embedder import *

load_dotenv()

PLAYLIST_LINK = "https://mediaspace.wisc.edu/playlist/dedicated/1_pdlead8k/1_krmy057m"

driver, download_dir = initialize_driver()

lecture_links = get_lessons(driver, PLAYLIST_LINK)
print(f"Found {len(lecture_links)} lectures")

conn = get_conn()

for filename in os.listdir(download_dir):
    file_path = os.path.join(download_dir, filename)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
        print(f"Deleted {file_path}")
    except Exception as e:
        print(f'Failed to delete {file_path}. Reason: {e}')


for lecture in lecture_links:
    link = lecture["lecture_link"]
    title = lecture["title"]
    lecture_id = generate_unique_int64(link)
    print(f"\nProcessing lecture: {title}")
    print(f"Link: {link}")

    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            page_info = scrape_lecture_page(driver, link, download_dir)
            if not page_info:
                raise Exception("No page info returned")

            date = page_info["date"]
            embed_link = page_info["embed_link"]
            chunks = parse_chunks(page_info["file_name"])

            chunk_ids = []
            embeddings = []
            for chunk in chunks:
                chunk_ids.append(generate_unique_int64(f"{link}-{chunk['index']}"))
                embeddings.append(embed_text(chunk["content"]))
            
            upload_clips(conn, lecture_id, chunk_ids, embeddings)
            
            # Success! Break out of retry loop
            break

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            
            # Clear the download directory
            for filename in os.listdir(download_dir):
                file_path = os.path.join(download_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    print(f"Cleaned up {file_path}")
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')

            # If this was the last attempt, continue to next lecture
            if attempt == max_attempts - 1:
                print(f"Failed to process lecture after {max_attempts} attempts, skipping: {link}")
                continue
            
            print("Retrying after short delay...")
            time.sleep(3)  # Wait a bit before retrying

driver.quit()
