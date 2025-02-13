# Adjust path for project root
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, project_root)

from backend.utils.scraper_tools.kaltura_scraper import *

link = "https://mediaspace.wisc.edu/media/Rebecca+Glawtschew-Ingraham+022-11+04+24-14%3A22%3A10/1_c64ijb9t"

driver, download_dir = initialize_driver()

print(scrape_lecture_page(driver, link, download_dir))

driver.quit()