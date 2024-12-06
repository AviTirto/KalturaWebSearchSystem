from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from query_manager import QueryManager
from crud import get_lesson_by_link
from data_types import Summary
import re


app = FastAPI()
qm = QueryManager()

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
        lesson = get_lesson_by_link(summary.link)
        output+=[
            {
                'start_time': summary.start_time,
                'end_time': summary.end_time,
                'embed_link': replace_start_time(lesson['metadatas'][0]['embed_link'], int(summary.seconds))
            }
        ]
    return output


    
