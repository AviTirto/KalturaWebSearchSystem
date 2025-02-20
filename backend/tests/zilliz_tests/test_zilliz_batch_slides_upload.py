import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, project_root)

from backend.utils.zilliz_tools.zilliz_api import upload_slides, get_conn
from backend.utils.encoders import generate_unique_int64
from backend.utils.embedder import embed_text
from backend.db.models import Slide
title = "PPT 1"

slides = [
    Slide(
        slide_id=generate_unique_int64(title + "-1"),
        page_num=1,
        ppt_id=1,
        text="This is the first slide",
    ),
    Slide(
        slide_id=generate_unique_int64(title + "-2"),
        page_num=2,
        ppt_id=1,
        text="This is the second slide",
    ),
]

embeddings = []
slides_ids = []
for slide in slides:
    embeddings.append(embed_text(slide.text))
    slides_ids.append(slide.slide_id)

print(slides_ids)

conn = get_conn()
upload_slides(conn, slides_ids, embeddings)


