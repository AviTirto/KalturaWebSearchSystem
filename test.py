import app.models.SQLModel.database as db
from app.models.ChromaModel.cdb import Storage
from app.services.query_manager import QueryManager
from app.services.lecture_manager import LectureManager
from app.utils.database_tools.crud import CRUDManager
from app.utils.scraping_tools.scraper import Scraper

session = db.get_session()
storage = Storage()
cm = CRUDManager(session, storage)
titles = cm.get_all_lecture_titles()
for title in titles:
    print(title)