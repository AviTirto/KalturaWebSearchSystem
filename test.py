import app.models.SQLModel.database as db
from app.models.ChromaModel.cdb import Storage
from app.services.query_manager import QueryManager
from app.services.lecture_manager import LectureManager
from app.utils.database_tools.crud import CRUDManager
from app.utils.scraping_tools.scraper import Scraper

# Get fresh session
session = db.get_session()
storage = Storage()
cm = CRUDManager(session, storage)

# First, clear ChromaDB
try:
    storage.db.delete_collection('embeddings')
    print("ChromaDB collections after delete:", storage.db.list_collections())
    # Recreate the embeddings collection to ensure clean state
    storage.embeddings = storage.db.get_or_create_collection(name="embeddings")
except Exception as e:
    print('ChromaDB clear error:', e)

# Then, clear SQLite database
try:
    # Clear in correct order due to foreign key constraints
    cm.delete_all_subtitles()
    cm.delete_all_lectures()
    session.commit()  # Make sure the deletions are committed
    print('SQL Model lectures remaining:', len(cm.get_all_lecture_titles()))
except Exception as e:
    print('SQLite clear error:', e)
    session.rollback()

# Now create new managers with fresh session
qm = QueryManager(db.get_session())
lm = LectureManager(db.get_session())

# Update lectures
lm.update_lectures()