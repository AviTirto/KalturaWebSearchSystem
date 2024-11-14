import os
from db import Storage
from scraper import Scraper
from parser import Parser
from dotenv import load_dotenv

load_dotenv()

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
        return [lesson['lecture_link'] for lesson in self.scraper.get_lessons(self.schedule_link)]

    def find_unsaved_lectures(self):
        saved_lectures = set(self.get_saved_lectures())
        updated_lectures = set(self.get_updated_lectures())
        return list(updated_lectures - saved_lectures)

    def remove_file(self, filename):
        os.remove(self.download_dir + '/' + filename)

    def update_lectures(self):
        unsaved_links = self.find_unsaved_lectures()
        for link in unsaved_links:
            page_info = self.scraper.scrape_lecture_page(link)
            chunks = self.parser.parse_chunks(page_info['file_name'])
            
            for index, chunk in enumerate(chunks):
                content = chunk['content']
                del chunk['content']
                self.db.add_lecture(chunk, content, link)

            del page_info['file_name']
            self.db.add_lesson(page_info, link)