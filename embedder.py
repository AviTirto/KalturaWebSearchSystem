import os
from dotenv import load_dotenv
import google.generativeai as genai
from chromadb.api.types import (
    Documents,
    EmbeddingFunction,
    Embeddings
)


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class Embedder(EmbeddingFunction):

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = genai.embed_content(
            model="models/text-embedding-004",
            content=input,
            task_type="document"
        )["embedding"]

        return embeddings
        