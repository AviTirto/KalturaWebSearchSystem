import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, project_root)

from typing import List
from backend.utils.zilliz_tools.zilliz_api import batch_slides_query
from backend.utils.firebase_tools.firebase_api import get_slide_metadata_batch
from backend.db.models import Slide
from backend.utils.gemini_tools.gemini_api import decide_slides_batch

async def slide_query(llm, conn, db, queries: List[str]):
    # Does a batch search on a list of query strings - returns a 2D array of selected chunk IDs
    retrieved_chunks = await batch_slides_query(conn, queries)

    # Convering 2D array of chunk IDs into a One dimensional list only having unique chunk id values
    unique_retrieved_chunks_ids = list({chunk for row in retrieved_chunks for chunk in row})
    
    # Query the firebase db with the chunk id values
    slides_metadata = await get_slide_metadata_batch(db, unique_retrieved_chunks_ids)

    batched_slides = []

    for chunks_list in retrieved_chunks:
        query_results = []
        for slide_id in chunks_list:
            chunk_json = slides_metadata[slide_id]
            chunk_json["slide_id"] = slide_id
            slide = Slide.model_validate(chunk_json)
            query_results.append(slide)
        batched_slides.append(query_results)
    
    selections = await decide_slides_batch(llm, batched_slides, queries)

    results = []
    for selection, slides in zip(selections, batched_slides):
        query_results = [(slides[index], reason) for index, reason in zip(selection.indexes, selection.reasons)]
        results.append(query_results)

    return results