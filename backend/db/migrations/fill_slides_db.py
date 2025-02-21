import os
import sys
import asyncio

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)

from backend.utils.cloudfareR2_tools.cloudfareR2_api import *
from backend.utils.encoders import pdf_to_images, generate_unique_int64
from backend.utils.gemini_tools.gemini_api import ocr_batch, get_ocr_llm
from backend.utils.embedder import embed_text
from backend.db.models import Slide, PPT
from backend.utils.zilliz_tools.zilliz_api import get_conn, upload_slides
from backend.utils.firebase_tools.firebase_api import get_db, add_slides_batch, add_ppts_batch

econ_dir_path = os.path.join(project_root, "Econ_301_PPT")
print(econ_dir_path)

ocr_llm = get_ocr_llm()
conn = get_conn()
db = get_db()
r2_client = get_cloudfareR2()

if os.path.exists(econ_dir_path):
    for path in os.listdir(econ_dir_path):
        print(path)
        file_path = os.path.join(econ_dir_path, path)
        title = path.replace(" ", "-")
        ppt_id = generate_unique_int64(title)

        # Convert PDF to images
        images_base64 = pdf_to_images(file_path)

        # OCR Batch
        print("Performing OCR...")
        ocr_results = asyncio.run(ocr_batch(ocr_llm, images_base64))
        print("OCR complete")

        # Make slides
        slides = []
        for i in range(len(ocr_results)):
            ocr_result = ocr_results[i]['result']
            slides.append(
                Slide(
                    slide_id=generate_unique_int64(f"{title}-{2*i + 1}"),
                    page_num = 2*i + 1,
                    text=ocr_result.slide_1_text,
                    ppt_id = ppt_id
                )
            )
            if ocr_result.slide_2_text:
                slides.append(
                    Slide(
                        slide_id=generate_unique_int64(f"{title}-{2*i + 2}"),
                        page_num = 2*i + 2,
                        text=ocr_result.slide_2_text,
                        ppt_id = ppt_id
                    )
                )

        # Zilliz Batch Insert
        embeddings = []
        slide_ids = []
        
        for slide in slides:
            embeddings.append(embed_text(slide.text))
            slide_ids.append(slide.slide_id)

        print("Uploading slides to Zilliz...")
        upload_slides(conn, slide_ids, embeddings)
        print("Upload complete")
        print("Zilliz insertion complete")

        # Firestore Batch Insert
        print("Inserting slides into Firestore...")
        add_slides_batch(db, slides)
        print("Firestore insertion complete")
        print("Inserting ppt into Firestore...")
        add_ppts_batch(db, [PPT(ppt_id=ppt_id, title=title, path = "Econ-301/" + title)])
        print("Firestore insertion complete")

        # R2 Batch Insert
        print("Uploading slides to R2...")
        with open(file_path, 'rb') as file:
            data = file.read()
            object_key = "Econ-301/" + path.replace(" ", "-") # Making format compatible with what R2 wants
            upload_file(r2_client, data, object_key)
        print("R2 upload complete")
        print(f"Successfully inserted {title}")


