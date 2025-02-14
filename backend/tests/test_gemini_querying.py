# Adjust path for project root
import sys
import os
import asyncio
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from dotenv import load_dotenv

load_dotenv()

from backend.utils.gemini_tools.gemini_api import *

llm = get_llm()

questions = ["What is docker", "What are some drawbacks to hadoop", "What is the difference between docker and kubernetes"]
sub_questions = asyncio.run(split_query_batch(llm, questions))

print(sub_questions)

