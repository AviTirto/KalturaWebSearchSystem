import sys
import os
import asyncio

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from backend.utils.zilliz_tools.zilliz_api import batch_clip_query, get_conn

queries = [
    "How do you compute the marginal rate of substitution?",
    "What is deadweight loss?",
    "Difference between engel curve of normal and inferior goods?"
]

conn = get_conn()

res = asyncio.run(batch_clip_query(conn, queries))
print(res)

