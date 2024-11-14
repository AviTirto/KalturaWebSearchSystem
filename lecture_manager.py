import os
from db import Storage
from scraper import Scraper
from lecture_parser import Parser
import base64
from dotenv import load_dotenv
import time

load_dotenv()

class LectureManager():
    def __init__(self):
        self.db = Storage()
        self.scraper = Scraper()
        self.schedule_link = 'https://tyler.caraza-harter.com/cs544/f23/schedule.html'
        self.download_dir = os.getenv('SRT_PATH')
        self.parser = Parser()

    def generate_unique_id(self, link, index):
        combined = f"{link}_{index}"
        return base64.urlsafe_b64encode(combined.encode()).decode()

    def get_saved_lectures(self):
        return self.db.get_lessons()

    def get_updated_lectures(self):
        return self.scraper.get_lessons(self.schedule_link)

    def find_unsaved_lectures(self):
        saved_lectures = set(self.get_saved_lectures())
        updated_lectures = self.get_updated_lectures()

        unsaved_lectures = [lesson for lesson in updated_lectures if lesson["lecture_link"] not in saved_lectures]

        return unsaved_lectures

    def remove_file(self, filename):
        os.remove(self.download_dir + '/' + filename)

    def update_lectures(self):
        unsaved_lectures = self.find_unsaved_lectures()

        for lecture in unsaved_lectures:
            link = lecture['lecture_link']

            page_info = self.scraper.scrape_lecture_page(link)
            chunks = self.parser.parse_chunks(page_info['file_name'])
            
            for index, chunk in enumerate(chunks):
                content = chunk['content']
                del chunk['content']
                uuid = self.generate_unique_id(link, index)
                self.db.add_lecture(chunk, content, uuid)

            del page_info['file_name']
            del lecture['lecture_link']
            
            self.db.add_lesson({**page_info, **lecture}, link)
            time.sleep(10)