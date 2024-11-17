import os
from dotenv import load_dotenv
import google.generativeai as genai
import chroma_db
from embedder import Embedder
from lecture_parser import Parser

load_dotenv()

# check out pylance

class Storage:
    def __init__(self):
        self.db = chroma_db.PersistentClient(
            path=os.getenv('LOCAL_DB_PATH')
        )

        self.embeddings = self.db.get_or_create_collection(
            name="embeddings",
            # embedding_function=Embedder()
        )

        
    def add_embeddings(self, chunk_id, subtitle):
        try:
            self.embeddings.add(
                ids = [chunk_id],
                documents = [subtitle],
            )
            return True
        except Exception as e:
            print(e)
            return False


    def vector_search(self, query, **kwargs):
        embeddings = kwargs.get('embedding', None)
        n_results = kwargs.get('n_results', 10)
        filter = kwargs.get('where', None)
        filter_document = kwargs.get('where_document', None)
        data = kwargs.get('include', ["metadatas", "documents"])

        return self.embeddings.query(
            query_embeddings = embeddings,
            n_results = n_results,
            where = filter,
            where_document = filter_document,
            query_texts = [query],
            include = data
        )




    