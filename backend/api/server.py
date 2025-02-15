# Server Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time
import re
import base64

app = FastAPI()
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


@app.get("/get_lecture_snippets")
async def get_lecture_snippets(query : str, key: str):
    pass


    