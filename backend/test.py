# Adjust path for project root
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, project_root)

from backend.utils.scraper_tools.kaltura_scraper import *

link = "https://mediaspace.wisc.edu/media/Rebecca+Glawtschew-Ingraham+022-11+20+24-14%3A21%3A17/1_rfnxplod"

driver, download_dir = initialize_driver()

scrape_lecture_page(driver, link, download_dir)

driver.quit()