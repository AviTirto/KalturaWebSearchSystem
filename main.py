from scraper import Scraper
from embedder import Embedder
from lecture_parser import Parser
from db import Storage
import os

# scraper = Scraper()
# srt_dir = scraper.execute()

# download_dir = os.getenv('SRT_PATH')
# embedder = Embedder(download_dir)
# embedder.embed("/Users/avitirto/Documents/ML/KalturaSearchSystem/lecture_srt/Tyler Caraza-Harter-Agriculture 125-09_04_24-14_18_34 (1).srt")

# p = Parser()
# c = p.parse_chunks("/Users/avitirto/Documents/ML/KalturaSearchSystem/lecture_srt/Tyler Caraza-Harter-Agriculture 125-09_04_24-14_18_34 (1).srt")
# print(c)

storage = Storage()
# storage.db.delete_collection("Lectures")
# print(storage.db.list_collections())
# storage.add_lecture("/Users/avitirto/Documents/ML/KalturaSearchSystem/lecture_srt/Tyler Caraza-Harter-Agriculture 125-09_04_24-14_18_34 (1).srt")

r = storage.query("What is the main difference between a CPU and GPU?")
print(r)
print(len(r))