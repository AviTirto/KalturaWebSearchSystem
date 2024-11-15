import os
from db import Storage
from scraper import Scraper
from lecture_parser import Parser
import base64
from dotenv import load_dotenv
import time

load_dotenv()

def generate_unique_id(link, index):
        combined = f"{link}_{index}"
        return base64.urlsafe_b64encode(combined.encode()).decode()

class LectureManager():
    def __init__(self):
        self.db = Storage()
        self.scraper = Scraper()
        self.schedule_link = 'https://tyler.caraza-harter.com/cs544/f23/schedule.html'
        self.download_dir = os.getenv('SRT_PATH')
        self.parser = Parser()

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
        os.remove(filename)


    # note! a way to remove failed lecture uploads from the db must be implemented
    def update_lectures(self):
        unsaved_lectures = self.find_unsaved_lectures()

        for lecture in unsaved_lectures:
            link = lecture['lecture_link']

            page_info = self.scraper.scrape_lecture_page(link)
            chunks = self.parser.parse_chunks(page_info['file_name'])
            
            for chunk in chunks:
                start = time.time()
                content = chunk['content']
                del chunk['content']
                uuid = generate_unique_id(link, chunk['index'])
                self.db.add_lecture({**chunk, **{'link':link}}, content, uuid)
                end = time.time()
                print(end - start)

            self.remove_file(page_info['file_name'])

            del page_info['file_name']
            
            self.db.add_lesson({**page_info, **lecture}, link)
            print(lecture)
