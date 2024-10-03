from scraper import Scraper
from embedder import Embedder
import os

# scraper = Scraper()
# srt_dir = scraper.execute()

download_dir = os.getenv('SRT_PATH')
embedder = Embedder(download_dir)
embedder.embed("/Users/avitirto/Documents/ML/KalturaSearchSystem/lecture_srt/Tyler Caraza-Harter-Agriculture 125-09_04_24-14_18_34 (1).srt")


