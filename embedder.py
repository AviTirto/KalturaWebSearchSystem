import os
from dotenv import load_dotenv
import google.generativeai as genai
from grpc import RpcError, StatusCode
from google.api_core.exceptions import ResourceExhausted
from tenacity import (
    retry, 
    stop_after_attempt, 
    wait_exponential, 
    retry_if_exception_type
)
from requests.exceptions import HTTPError
from chromadb.api.types import (
    Documents,
    EmbeddingFunction,
    Embeddings
)


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class Embedder(EmbeddingFunction):

    @retry(
        retry=retry_if_exception_type(ResourceExhausted),
        stop=stop_after_attempt(5),  # Retry up to 5 times
        wait=wait_exponential(multiplier=1, min=20, max=30) 
    )
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
        