from typing import List
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from backend.services.clip_query_service import *
from backend.utils.zilliz_tools.zilliz_api import *
from backend.utils.gemini_tools.gemini_api import *
from backend.utils.firebase_tools.firebase_api import *

queries = [
    "How do you compute the marginal rate of substitution?",
    "What is deadweight loss?",
    "Difference between engel curve of normal and inferior goods?"
]


res = asyncio.run(clip_query(get_llm(), get_conn(), get_db(), queries))
print(res)