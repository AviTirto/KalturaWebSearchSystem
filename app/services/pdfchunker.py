from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict
import numpy as np
from app.utils.gemini_tools.queryer import Queryer


class PDFChunker:
    def __init__(self, max_chunk_size: int = 500):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.max_chunk_size = max_chunk_size
        self.queryer = Queryer()

    def chunk_pdf(self, pdf_pages: List[str]) -> List[Dict[str, str]]:
        all_text = "\n".join(pdf_pages)
        sentences = all_text.split(". ")
        tfidf_matrix = self.vectorizer.fit_transform(sentences)
        sentence_scores = np.mean(tfidf_matrix.toarray(), axis=1)

        chunks = []
        current_chunk = ""
        current_length = 0

        for i, sentence in enumerate(sentences):
            if current_length + len(sentence) > self.max_chunk_size:
                chunk_prompt = f"Detect logical chunking points in the following text:\n{current_chunk}"
                chunk_boundaries = self.queryer.call_llm(chunk_prompt)
                split_chunks = self.split_text_by_boundaries(current_chunk, chunk_boundaries)
                chunks.extend(split_chunks)
                current_chunk = sentence + ". "
                current_length = len(sentence)
            else:
                current_chunk += sentence + ". "
                current_length += len(sentence)

        if current_chunk:
            chunk_prompt = f"Detect logical chunking points in the following text:\n{current_chunk}"
            chunk_boundaries = self.queryer.call_llm(chunk_prompt)
            split_chunks = self.split_text_by_boundaries(current_chunk, chunk_boundaries)
            chunks.extend(split_chunks)

        return chunks

    def split_text_by_boundaries(self, text: str, boundaries: List[int]) -> List[Dict[str, str]]:
        split_chunks = []
        start = 0

        for boundary in boundaries:
            split_chunks.append({"content": text[start:boundary]})
            start = boundary

        if start < len(text):
            split_chunks.append({"content": text[start:]})

        return split_chunks
