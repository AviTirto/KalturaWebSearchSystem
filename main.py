from scraper import Scraper
# from embedder import Embedder
from lecture_parser import Parser
from lecture_manager import LectureManager, generate_unique_id
from db import Storage
from query_manager import QueryManager
import os

# manager = LectureManager()
# manager.update_lectures()

# storage = Storage()
# lessons = storage.get_lessons()
# for lesson in lessons:
#     print(lesson)

# storage.db.delete_collection('Lessons')
# storage.db.delete_collection('Lectures')
# print(storage.db.list_collections())


# print('---------------------------------------------')

# print(results['documents'][0])


# srt_dir = scraper.execute()
# scraper.get_embed_link("https://mediaspace.wisc.edu/media/Tyler%20Caraza-Harter-Agriculture%20125-09_04_24-14%3A18%3A34/1_sbftfkbl")

# download_dir = os.getenv('SRT_PATH')
# embedder = Embedder(download_dir)
# embedder.embed("/Users/avitirto/Documents/ML/KalturaSearchSystem/lecture_srt/Tyler Caraza-Harter-Agriculture 125-09_04_24-14_18_34 (1).srt")

# p = Parser()
# c = p.parse_chunks("/Users/avitirto/Documents/ML/KalturaSearchSystem/lecture_srt/Tyler Caraza-Harter-Agriculture 125-09_04_24-14_18_34 (1).srt")
# print(c)

# storage = Storage()
# storage.db.delete_collection("Lectures")
# print(storage.db.list_collections())
# storage.add_lecture("/Users/avitirto/Documents/ML/KalturaSearchSystem/lecture_srt/Tyler Caraza-Harter-Agriculture 125-09_04_24-14_18_34 (1).srt")

# r = storage.query("What is the main difference between a CPU and GPU?")
# print(r)
# print(len(r))