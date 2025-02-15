# Server Imports
from fastapi import FastAPI, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import re
import asyncio
import uuid
from typing import List, Dict

import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from backend.services.clip_query_service import clip_query
from backend.utils.zilliz_tools.zilliz_api import get_conn
from backend.utils.firebase_tools.firebase_api import get_db, get_lecture_batch
from backend.utils.gemini_tools.gemini_api import get_llm

app = FastAPI()
query_queue = asyncio.Queue()
response_map: Dict[str, asyncio.Future] = {}
batch_size = 10
batch_timeout = 10

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

@app.get("/search_clips")
async def get_lecture_snippets(query: str):
    request_id = str(uuid.uuid4())  # Generate unique request identifier
    future = asyncio.get_event_loop().create_future()
    response_map[request_id] = future
    
    await query_queue.put((request_id, query))  # Add query with its identifier
    
    response = await future  # Wait for response
    del response_map[request_id]  # Cleanup
    return response

async def process_queries():
    while True:
        batch = []
        request_ids = []
        try:
            first_request = await asyncio.wait_for(query_queue.get(), timeout=batch_timeout)
            request_ids.append(first_request[0])
            batch.append(first_request[1])
            
            while len(batch) < batch_size:
                try:
                    req_id, query = await asyncio.wait_for(query_queue.get(), timeout=batch_timeout)
                    request_ids.append(req_id)
                    batch.append(query)
                except asyncio.TimeoutError:
                    break

            llm = get_llm()
            conn = get_conn()
            db = get_db()
            
            # Call the middleware function
            clip_results = await clip_query(llm, conn, db, batch)
            
            # Collect unique lecture IDs
            lecture_ids = list({subtitle.lecture_id for response in clip_results for subtitle, _ in response})
            lecture_metadata = await get_lecture_batch(db, lecture_ids)
            
            # Process results for each query
            for req_id, query_results in zip(request_ids, clip_results):
                response_json = []
                for subtitle, explanation in query_results:
                    embed_link = replace_start_time(lecture_metadata[subtitle.lecture_id]["embed_link"], subtitle.seconds)
                    response_json.append({
                        "start_time": subtitle.start_time,
                        "end_time": subtitle.end_time,
                        "embed_link": embed_link,
                        "explanation": explanation
                    })
                
                if req_id in response_map:
                    response_map[req_id].set_result(response_json)  # Send response back to the request
        except asyncio.TimeoutError:
            continue

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_queries())
