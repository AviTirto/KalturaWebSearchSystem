# Server Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# Search System Modules
from app.services.query_manager import QueryManager
from app.utils.database_tools.crud import CRUDManager
from app.models.ChromaModel.cdb import Storage
import app.models.SQLModel.database as db
from app.services.lecture_manager import LectureManager

# General Python Libraries
import time
import re

scheduler = BackgroundScheduler()
app = FastAPI()
qm = QueryManager(db.get_session())
lm = LectureManager(db.get_session())
storage = Storage()
crud_manager = CRUDManager(db.get_session(), storage)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace with specific domains in production.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


def update_db():
    """Task to update the database."""
    try:
        print(f"Starting database update at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        # lm.update_lectures()
        print(f"Database update completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"Error updating database: {e}")

def replace_start_time(input_string, replacement_number):
    # Regular expression to find the pattern `startTime` followed by any characters and then a `0`
    pattern = r"(startTime.*?A)0"
    # Replace the matched 0 with the replacement_number
    updated_string = re.sub(pattern, rf"\g<1>{replacement_number}", input_string)
    return updated_string

@app.on_event('startup')
def on_startup():
    db.init_db()
    print('starting scheduler...')
    scheduler.add_job(update_db, CronTrigger(hour=0, minute=0))

    # try:
    #     storage.db.delete_collection('embeddings')
    #     print('ChromaDB Tables:', storage.db.list_collections())
    # except:
    #     print('embedding table not initialized, nothing to clear')


    # crud_manager.delete_all_lectures()
    # print('SQL Model Tables:', crud_manager.get_all_lecture_titles())

    # update_db()
    scheduler.start()

@app.on_event('shutdown')
def on_shutdown():
    """Shut down the scheduler."""
    print("Shutting down scheduler...")
    scheduler.shutdown()


@app.get("/")
async def get_lecture_snippets(query : str, key: str):
    qm.set_key(key)
    summaries = qm.query(query)

    output = []
    for summary in summaries:
        lecture = crud_manager.get_lecture_metadata(summary["lecture_id"])
        output+=[
            {
                'start_time': summary["start_time"],
                'end_time': summary["end_time"],
                'embed_link': replace_start_time(lecture.embed_link, int(summary["seconds"]))
            }
        ]
    return output


    
