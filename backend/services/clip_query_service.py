from typing import List
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, project_root)

from backend.utils.zilliz_tools.zilliz_api import *

import asyncio

async def query(conn, db, queries: List[str]):
    subtitle_chunks_list = []

    results = self.queryer.decide_subtitles(summaries, input)
    indexes = results.indexes
    reasons = results.reasons

    output = []
    for i, r in zip(indexes, reasons):
        output.append((summaries[i], r))

    return output