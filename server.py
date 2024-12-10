from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from query_manager import QueryManager
from crud import CRUDManager
import re
from cdb import Storage
import database as db


app = FastAPI()
qm = QueryManager(db.get_session())
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

def replace_start_time(input_string, replacement_number):
    # Regular expression to find the pattern `startTime` followed by any characters and then a `0`
    pattern = r"(startTime.*?A)0"
    # Replace the matched 0 with the replacement_number
    updated_string = re.sub(pattern, rf"\g<1>{replacement_number}", input_string)
    return updated_string


@app.get("/")
async def get_lecture_snippets(query : str):
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


    
