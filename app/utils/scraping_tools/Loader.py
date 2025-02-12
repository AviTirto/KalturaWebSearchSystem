from pdf2image import convert_from_path
import re
import io
import base64

class Loader:
    def __init__(self):
        pass

    # Convert PDF to images (one image per page)
    def pdf_to_images(self, pdf_path):
        images = convert_from_path(pdf_path)  # Convert all PDF pages to images
        if not images:
            return None
        return images
    
    # Convert an image to a base64-encoded string
    def image_to_base64(self, image):
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="JPEG")  # Save the image as JPEG
        img_bytes = img_bytes.getvalue()

        # Convert image to base64
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        return img_base64

    def clean_text_for_rag(self, raw_text):
        """Cleans raw text for RAG system: keeps only letters, numbers, and selected symbols, while removing standalone number lines."""
        
        # Define allowed characters
        allowed_chars = r'a-zA-Z0-9+\-*/=<>∑√∞∫≈≠≤≥$%,.\*\(\)\[\]\{\}'

        # Define Unicode ranges for mathematical alphanumeric symbols and numbers
        allowed_unicode = r'\U0001D400-\U0001D7FF\U0001D7CE-\U0001D7FF'

        # Remove all characters **not** in the allowed set
        cleaned_text = re.sub(fr'[^{{allowed_chars}}{{allowed_unicode}}\s]', '', raw_text)

        return cleaned_text

