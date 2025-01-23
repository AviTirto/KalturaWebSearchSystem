import app.models.SQLModel.database as db
from app.models.ChromaModel.cdb import Storage
from app.services.query_manager import QueryManager
from app.services.lecture_manager import LectureManager
from app.utils.database_tools.crud import CRUDManager
from app.utils.scraping_tools.scraper import Scraper
import base64

# Get fresh session
session = db.get_session()
storage = Storage()
cm = CRUDManager(session, storage)
scraper = Scraper()

cm.delete_all_lectures()
cm.delete_all_subtitles()

link = "https://mediaspace.wisc.edu/media/Tyler%20Caraza-Harter-Agriculture%20125-11_27_24-14%3A23%3A05/1_s00iopqh"
meta_data = scraper.scrape_lecture_page(link)
print(meta_data['file_name'])

lm = LectureManager(session)

lm.update_lectures()

link = "https://mediaspace.wisc.edu/media/Tyler%20Caraza-Harter-Agriculture%20125-11_27_24-14%3A23%3A05/1_s00iopqh"

lecture_id = base64.urlsafe_b64encode(link.encode()).decode()

subtitles = cm.get_all_subtitles_by_lecture(lecture_id)

for subtitle in subtitles:
    print(base64.urlsafe_b64decode(subtitle.chunk_id).decode())




