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
from backend.services.slides_query_service import slide_query
from backend.utils.zilliz_tools.zilliz_api import get_conn
from backend.utils.firebase_tools.firebase_api import get_db, get_lecture_batch, get_ppt_batch, postFeedback
from backend.utils.gemini_tools.gemini_api import get_llm
from backend.db.models import UserFeedback

# Configuration
BATCH_SIZE = 10 
BATCH_TIMEOUT = 0.1 

@dataclass
class PendingRequest:
    query: str
    future: asyncio.Future
    timestamp: datetime

# Global state for clip requests
clip_request_queue: asyncio.Queue[PendingRequest] = asyncio.Queue()
processor_task = None

# Global state for slide requests
slide_request_queue: asyncio.Queue[PendingRequest] = asyncio.Queue()
slide_processor_task = None

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

async def process_clip_batch():
    """Background task that processes clip requests in batches"""
    # Initialize connections once for the processor
    llm = get_llm()
    conn = get_conn()
    db = get_db()
    
    try:
        while True:
            batch: List[PendingRequest] = []
            
            # Get the first request
            first_request = await clip_request_queue.get()
            batch.append(first_request)
            
            # Try to fill the batch
            batch_start = datetime.now()
            while len(batch) < BATCH_SIZE:
                try:
                    # Wait for more requests, but not too long
                    request = await asyncio.wait_for(
                        clip_request_queue.get(), 
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
                clip_request_queue.task_done()
                
    finally:
        conn.close()

async def process_slide_batch():
    """Background task that processes slide requests in batches"""
    # Initialize connections once for the processor
    llm = get_llm()
    conn = get_conn()
    db = get_db()
    
    try:
        while True:
            batch: List[PendingRequest] = []
            
            # Get the first request
            first_request = await slide_request_queue.get()
            batch.append(first_request)
            
            # Try to fill the batch
            batch_start = datetime.now()
            while len(batch) < BATCH_SIZE:
                try:
                    # Wait for more requests, but not too long
                    request = await asyncio.wait_for(
                        slide_request_queue.get(), 
                        timeout=BATCH_TIMEOUT
                    )
                    batch.append(request)
                except asyncio.TimeoutError:
                    break
            
            # Process the batch
            queries = [req.query for req in batch]
            try:
                slide_results = await slide_query(llm, conn, db, queries)
                
                ppt_ids = list({
                    slide.ppt_id 
                    for response in slide_results 
                    for slide, _ in response
                })
                ppt_metadata = await get_ppt_batch(db, ppt_ids)

                # Process slide results and set them for each request
                for request, results in zip(batch, slide_results):
                    response_json = []
                    for slide, explanation in results:
                        response_json.append({
                            "title": ppt_metadata[slide.ppt_id]["title"],
                            "page_num": slide.page_num,
                            "text": slide.text,
                            "path": ppt_metadata[slide.ppt_id]["path"],
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
                slide_request_queue.task_done()
                
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
    
    # Add to clip queue
    await clip_request_queue.put(request)
    
    # Wait for result
    return await future

@app.get("/search_slides")
async def get_slide_snippets(query: str):
    # Create a future for this request
    future = asyncio.get_running_loop().create_future()
    request = PendingRequest(
        query=query,
        future=future,
        timestamp=datetime.now()
    )
    
    # Add to queue
    await slide_request_queue.put(request)
    
    # Wait for result
    return await future

@app.on_event("startup")
async def startup_event():
    global processor_task, slide_processor_task

    # Initialize connections early to avoid first-request failures
    global llm, conn, db
    llm = get_llm()
    conn = get_conn()
    db = get_db()

    # Warm-up test query to ensure the connection is live
    try:
        _ = await clip_query(llm, conn, db, ["warm-up query"])
    except Exception as e:
        print(f"Warning: Warm-up query failed: {e}")

    # Start background tasks
    processor_task = asyncio.create_task(process_clip_batch())
    slide_processor_task = asyncio.create_task(process_slide_batch())


@app.on_event("shutdown")
async def shutdown_event():
    if processor_task:
        processor_task.cancel()
        try:
            await processor_task
        except asyncio.CancelledError:
            pass
    if slide_processor_task:
        slide_processor_task.cancel()
        try:
            await slide_processor_task
        except asyncio.CancelledError:
            pass

@app.post("/postFeedback")
async def post_feedback(quesion, thumbs_up_count, thumbs_down_count, total_count):
    user_feedback = UserFeedback(
        question=quesion,
        thumbs_up_count=thumbs_up_count,
        thumbs_down_count = thumbs_down_count, 
        total_count = total_count
    )

    db = get_db()
    postFeedback(db, user_feedback)
