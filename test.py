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

storage.db.delete_collection('embeddings')

lm = LectureManager(session)

lm.update_lectures()






