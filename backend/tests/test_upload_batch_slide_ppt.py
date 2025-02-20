import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from backend.utils.firebase_tools.firebase_api import get_db, add_slides_batch, add_ppts_batch
from backend.db.models import Slide, PPT

db = get_db()

slides = [
    Slide(
        slide_id=1,
        page_num=1,
        ppt_id=1,
        text="This is the first slide",
    ),
    Slide(
        slide_id=2,
        ppt_id=2,
        page_num=2,
        text="This is the second slide",
    ),
]

ppts = [
    PPT(
        ppt_id=1,
        title="This is the first ppt",
        path="This is the first ppt",
    ),
    PPT(
        ppt_id=2,
        title="This is the second ppt",
        path="This is the second ppt",
    )
]

add_slides_batch(db, slides)
add_ppts_batch(db, ppts)
