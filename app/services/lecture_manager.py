import os
from app.models.ChromaModel.cdb import Storage
from app.utils.scraping_tools.scraper import Scraper
from app.utils.scraping_tools.lecture_parser import Parser
import base64
from dotenv import load_dotenv
from app.utils.database_tools.crud import CRUDManager
from app.models.SQLModel.models import Subtitles, Lecture
from sqlmodel import Session

load_dotenv()

def generate_unique_chunk_id(link, index):
    combined = f"{link}_{index}"
    return base64.urlsafe_b64encode(combined.encode()).decode()

def generate_unique_lecture_id(link):
    return base64.urlsafe_b64encode(link.encode()).decode()

class LectureManager():
    def __init__(self, session : Session):
        self.db = Storage() # This references the chroma DB database
        self.scraper = Scraper()
        self.schedule_link = 'https://tyler.caraza-harter.com/cs544/f24/schedule.html'
        self.download_dir = os.getenv('SRT_PATH')
        self.parser = Parser()
        self.crud_manager = CRUDManager(session, self.db)

    def get_saved_lectures(self):
        return self.crud_manager.get_all_lecture_ids()

    def get_updated_lectures(self):
        return self.scraper.get_lessons(self.schedule_link)

    def find_unsaved_lectures(self):
        saved_lectures = set(self.get_saved_lectures())
        updated_lectures = self.get_updated_lectures()
        unsaved_lectures = [lesson for lesson in updated_lectures if generate_unique_lecture_id(lesson["lecture_link"]) not in saved_lectures]
        return unsaved_lectures

    def remove_file(self, filename):
        os.remove(filename)

    # note! a way to remove failed lecture uploads from the db must be implemented
    # This function will change quite a bit
    def update_lectures(self):
        unsaved_lectures = self.find_unsaved_lectures()

        for lecture in unsaved_lectures:
            link = lecture['lecture_link']
            title = lecture['title']
            lecture_id = generate_unique_lecture_id(link)

            page_info = self.scraper.scrape_lecture_page(link)

            if not page_info:
                continue

            date = page_info['date']
            embed_link = page_info['embed_link']
            chunks = self.parser.parse_chunks(page_info['file_name'])
            
            for chunk in chunks:
                chunk_id = generate_unique_chunk_id(link, chunk['index'])
                # Add subtitle metadata
                subtitle_data = {
                    "chunk_id": chunk_id,
                    "index": chunk['index'],
                    "subtitle": chunk['content'],
                    "start_time": chunk['start_time'],
                    "end_time": chunk['end_time'],
                    "seconds": chunk['seconds'],
                    "lecture_id": lecture_id
                }
                self.crud_manager.add_subtitle_metadata(subtitle_data)
                self.db.add_embeddings(chunk_id=chunk_id, subtitle=chunk['content'])
                print('Current Number of Embeddings:', self.db.embeddings.count())

            self.remove_file(page_info['file_name'])
            del page_info['file_name']

            lecture_data = {
                "lecture_id": lecture_id,  # Ensure 'id' exists in lecture data
                "date": date,
                "title": title,
                "embed_link": embed_link
            }
            self.crud_manager.add_lecture_metadata(lecture_data)
