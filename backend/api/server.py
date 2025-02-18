from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re
import asyncio
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime

import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from backend.services.clip_query_service import clip_query
from backend.utils.zilliz_tools.zilliz_api import get_conn
from backend.utils.firebase_tools.firebase_api import get_db, get_lecture_batch
from backend.utils.gemini_tools.gemini_api import get_llm

# Configuration
BATCH_SIZE = 10 
BATCH_TIMEOUT = 0.1 

@dataclass
class PendingRequest:
    query: str
    future: asyncio.Future
    timestamp: datetime

# Global state
request_queue: asyncio.Queue[PendingRequest] = asyncio.Queue()
processor_task = None

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def replace_start_time(input_string, replacement_number):
    pattern = r"(startTime.*?A)0"
    updated_string = re.sub(pattern, rf"\g<1>{replacement_number}", input_string)
    return updated_string

async def process_batch():
    """Background task that processes requests in batches"""
    # Initialize connections once for the processor
    llm = get_llm()
    conn = get_conn()
    db = get_db()
    
    try:
        while True:
            batch: List[PendingRequest] = []
            
            # Get the first request
            first_request = await request_queue.get()
            batch.append(first_request)
            
            # Try to fill the batch
            batch_start = datetime.now()
            while len(batch) < BATCH_SIZE:
                try:
                    # Wait for more requests, but not too long
                    request = await asyncio.wait_for(
                        request_queue.get(), 
                        timeout=BATCH_TIMEOUT
                    )
                    batch.append(request)
                except asyncio.TimeoutError:
                    break
            
            # Process the batch
            queries = [req.query for req in batch]
            try:
                clip_results = await clip_query(llm, conn, db, queries)
                
                # Get all unique lecture IDs from the results
                lecture_ids = list({
                    subtitle.lecture_id 
                    for response in clip_results 
                    for subtitle, _ in response
                })
                lecture_metadata = await get_lecture_batch(db, lecture_ids)
                
                # Set results for each request in the batch
                for request, results in zip(batch, clip_results):
                    response_json = []
                    for subtitle, explanation in results:
                        embed_link = replace_start_time(
                            lecture_metadata[subtitle.lecture_id]["embed_link"], 
                            subtitle.seconds
                        )
                        response_json.append({
                            "start_time": subtitle.start_time,
                            "end_time": subtitle.end_time,
                            "embed_link": embed_link,
                            "explanation": explanation
                        })
                    request.future.set_result(response_json)
                    
            except Exception as e:
                # If processing fails, set exception for all requests in batch
                for request in batch:
                    if not request.future.done():
                        request.future.set_exception(e)
            
            # Mark tasks as done in the queue
            for _ in batch:
                request_queue.task_done()
                
    finally:
        conn.close()

@app.get("/search_clips")
async def get_lecture_snippets(query: str):
    # Create a future for this request
    future = asyncio.get_running_loop().create_future()
    request = PendingRequest(
        query=query,
        future=future,
        timestamp=datetime.now()
    )
    
    # Add to queue
    await request_queue.put(request)
    
    # Wait for result
    return await future

@app.on_event("startup")
async def startup_event():
    global processor_task
    processor_task = asyncio.create_task(process_batch())

@app.on_event("shutdown")
async def shutdown_event():
    if processor_task:
        processor_task.cancel()
        try:
            await processor_task
        except asyncio.CancelledError:
            pass
