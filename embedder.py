import os
from dotenv import load_dotenv
import google.generativeai as genai
from grpc import RpcError, StatusCode
from google.api_core.exceptions import ResourceExhausted
from requests.exceptions import HTTPError
from chromadb.api.types import (
    Documents,
    EmbeddingFunction,
    Embeddings
)
from google.api_core import retry


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class Embedder(EmbeddingFunction):

    @retry.Retry(timeout=300.0)
    def __call__(self, input: Documents) -> Embeddings:
        try:
            embeddings = genai.embed_content(
                model="models/text-embedding-004",
                content=input,
                task_type="question_answering"
            )["embedding"]
            return embeddings
        except ResourceExhausted as e:
            print("Resource exhausted. Retrying...")
            raise  # Raise to trigger tenacity retry
        except RpcError as e:
            if e.code() == StatusCode.RESOURCE_EXHAUSTED:
                print("Resource exhausted. Retrying...")
                raise  # Raise to trigger tenacity retry
            else:
                raise  # Re-raise other RpcErrors without retrying
        