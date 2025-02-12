import os
import base64
from dotenv import load_dotenv
from app.utils.scraping_tools.Loader import Loader
from app.utils.gemini_tools.ocr import OCRModel
from app.models.ChromaModel.records import PPTcdb
from app.utils.gemini_tools.ppt_types import PPT, Slide

load_dotenv()

class PPTManager:
    def __init__(self):
        self.pdf_directory = "./Econ_301_PPT/"

        print(f"Resolved path: {self.pdf_directory}")
        print(f"Exists? {os.path.exists(self.pdf_directory)}")

        self.pdf_files = [os.path.join(self.pdf_directory, f) for f in os.listdir(self.pdf_directory) if f.endswith(".pdf")]
        self.loader = Loader()
        self.ocr_model = OCRModel()
        self.cdb = PPTcdb()

    def generate_unique_chunk_id(self, title, page_num):
        combined = f"{title}_{page_num}"
        return base64.urlsafe_b64encode(combined.encode()).decode()

    def parse_ppt(self, file_path: str) -> PPT:
        ppt = PPT(title=file_path, slides=[])
        images = self.loader.pdf_to_images(file_path)
        total_input_tokens = 0
        total_output_tokens = 0

        for i in range(len(images)):
            print(f'{ppt.title} {i}')
            response = self.ocr_model.extract_text(self.loader.image_to_base64(images[i]))
            ocr_result = response['result']
            total_input_tokens += response['input_tokens']
            total_output_tokens += response['output_tokens']

            slide1 = Slide(
                id=self.generate_unique_chunk_id(file_path, 2*i + 1),
                page_num=i+1,
                rag_text=ocr_result.slide_1_text,
            )

            ppt.slides += [slide1]

            if ocr_result.slide_2_text:
                slide2 = Slide(
                    id=self.generate_unique_chunk_id(file_path, 2*i + 2),
                    page_num=i+1,
                    rag_text=ocr_result.slide_2_text,
                )

                ppt.slides += [slide2]

        return ppt, total_input_tokens, total_output_tokens
        
    def add_ppt(self, ppt: PPT):
        for slide in ppt.slides:
            try:
                self.cdb.add_slide(id = slide.id, title = ppt.title, page_num = slide.page_num, rag_text = slide.rag_text)
            except:
                print(f'Error in PPT: {ppt.title} on slide: {slide.page_num}')

        return True

    def populate_ppts(self):
        for file in self.pdf_files:
            ppt, total_input_tokens, total_output_tokens = self.parse_ppt(file)
            print('Total Input Tokens:', total_input_tokens)
            print('Total Output Tokens:', total_output_tokens)
            print(ppt.title)
            self.add_ppt(ppt)

    def query(self, prompt):
        response = self.cdb.vector_search(prompt)
        metadatas = response['metadatas'][0]
        documents = response['documents'][0]
    
        return {
            'titles': [metadata['title'] for metadata in metadatas],
            'page_nums': [metadata['page_num'] for metadata in metadatas],
            'texts': documents
        }