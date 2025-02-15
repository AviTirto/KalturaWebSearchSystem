from typing import List
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, project_root)

from backend.utils.zilliz_tools.zilliz_api import *
from backend.utils.firebase_tools.firebase_api import *
from backend.db.models import Lecture, Subtitle
from backend.utils.gemini_tools.gemini_api import *

import asyncio

async def clip_query(llm, conn, db, queries: List[str]):
    # Does a batch search on a list of query strings - returns a 2D array of selected chunk IDs
    retrieved_chunks = await batch_clip_query(conn, queries)

    # Convering 2D array of chunk IDs into a One dimensional list only having unique chunk id values
    unique_retrieved_chunks_ids = list({chunk for row in retrieved_chunks for chunk in row})
    
    # Query the firebase db with the chunk id values
    clips_metadata = get_subtitle_metadata_batch(db, unique_retrieved_chunks_ids)

    batched_subtitles = []

    for chunks_list in retrieved_chunks:
        query_results = []
        for chunk_id in chunks_list:
            chunk_json = clips_metadata[chunk_id]
            chunk_json["chunk_id"] = chunk_id
            #print(chunk_json)
            #subtitle = Subtitle.model_validate(chunk_json)
            #subtitle = Subtitle(**chunk_json)
            subtitle = Subtitle.model_validate(chunk_json)
            query_results.append(subtitle)
        batched_subtitles.append(query_results)
    
    selections = await decide_subtitles_batch(llm, batched_subtitles, queries)

    results = []
    for selection, subtitles in zip(selections, batched_subtitles):
        query_results = [(subtitles[index], reason) for index, reason in zip(selection.indexes, selection.reasons)]
        results.append(query_results)

    return results