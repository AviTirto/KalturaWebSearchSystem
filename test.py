import app.models.SQLModel.database as db
from app.models.ChromaModel.cdb import Storage
from app.services.query_manager import QueryManager
from app.services.lecture_manager import LectureManager
from app.utils.database_tools.crud import CRUDManager
from app.utils.scraping_tools.scraper import Scraper

db.init_db()
qm = QueryManager(db.get_session())
lm = LectureManager(db.get_session())
storage = Storage()
cm = CRUDManager(db.get_session(), storage)

# try:
#     storage.db.delete_collection('embeddings')
#     print("ChromaDB",storage.db.list_collections())
# except:
#     print('no cache')


# cm.delete_all_lectures()
# cm.delete_all_subtitles()
print('SQL Model:', len(cm.get_all_lecture_titles()))


# lm.update_lectures()
