import os
import sys
import asyncio
from backend.db.models import UserFeedback
from backend.utils.firebase_tools.firebase_api import postFeedback, get_db
from dotenv import load_dotenv

load_dotenv()

user_feedback = UserFeedback(
    question="What is deadweight loss?",
    thumbs_up_count=3,
    thumbs_down_count=1,
    total_count=5
)

async def test_post_feedback():
    db = get_db()
    await postFeedback(db, user_feedback) 

asyncio.run(test_post_feedback())
