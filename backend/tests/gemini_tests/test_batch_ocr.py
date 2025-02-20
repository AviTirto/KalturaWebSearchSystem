import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from backend.utils.gemini_tools.gemini_api import ocr_batch, get_ocr_llm
from pdf2image import convert_from_path
import io
import base64
import asyncio

ocr_llm = get_ocr_llm()

pdf = [
    "/Users/avitirto/Documents/ML/KalturaSearchSystem/Econ_301_PPT/Chapter 1 PPT.pdf",
]

images = convert_from_path(pdf[0])

images_base64 = []
for image in images:
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")  # Save the image as JPEG
    img_bytes = img_bytes.getvalue()
    images_base64.append(base64.b64encode(img_bytes).decode("utf-8"))

ocr_result = asyncio.run(ocr_batch(ocr_llm, images_base64))

i = 1
for result in ocr_result:
    print('Slide: ', i)
    i += 1
    print('Slide 1:')
    print(result['result'].slide_1_text)
    if result['result'].slide_2_text:
        print('Slide 2:')
        print(result['result'].slide_2_text)
    print("-"*100)
