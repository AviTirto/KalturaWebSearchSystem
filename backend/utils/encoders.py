import hashlib
from pdf2image import convert_from_path
import io
import base64

def generate_unique_int64(input_string):
    sha256_hash = hashlib.sha256(input_string.encode('utf-8')).hexdigest()
    
    int64_value = int(sha256_hash[:15], 16)
    
    MAX_INT64 = 9223372036854775807  
    int64_value = int64_value % MAX_INT64

    return int64_value

def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    images_base64 = []
    for image in images:
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="JPEG")  # Save the image as JPEG
        img_bytes = img_bytes.getvalue()
        images_base64.append(base64.b64encode(img_bytes).decode("utf-8"))
    return images_base64

