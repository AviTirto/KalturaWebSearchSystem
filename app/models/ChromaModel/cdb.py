import os
from dotenv import load_dotenv
import google.generativeai as genai
import chromadb
from app.utils.gemini_tools.embedder import Embedder
from app.utils.scraping_tools.lecture_parser import Parser

load_dotenv()

# check out pylance

class Storage:
    def __init__(self):
        self.db = chromadb.PersistentClient(
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
        n_results = kwargs.get('n_results', 5)
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
    
    def get_embedding(self, **kwargs):
        ids = kwargs.get('ids', None)
        where = kwargs.get('where', None)
        return self.embeddings.get(
            ids = ids,
            where = where
        )




    