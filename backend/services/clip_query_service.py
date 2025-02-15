from typing import List
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, project_root)

from backend.utils.zilliz_tools.zilliz_api import *
from backend.utils.firebase_tools.firebase_api import *

import asyncio

async def clip_query(conn, db, queries: List[str]):
    # Does a batch search on a list of query strings - returns a 2D array of selected chunk IDs
    retrieved_chunks = await batch_clip_query(conn, queries)

    # Convering 2D array of chunk IDs into a One dimensional list only having unique chunk id values
    unique_retrieved_chunks_ids = list({chunk for row in retrieved_chunks for chunk in row})

    # Get the corresponding lecture ids from unique_retrieved_chunk_ids
    
    
    # Query the firebase db with the chunk id values
    clips = get_subtitle_metadata_batch(db, unique_retrieved_chunks_ids)
    return clips