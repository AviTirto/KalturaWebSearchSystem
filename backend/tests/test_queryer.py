# Adjust path for project root
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)
from backend.utils.gemini_tools.queryer import *

def test_split_query_batch(questions):
    result = asyncio.run(split_query_batch(questions))
    return result

sub_questons = test_split_query_batch(["What is docker", "What are some drawbacks to hadoop"])
print(sub_questons)

