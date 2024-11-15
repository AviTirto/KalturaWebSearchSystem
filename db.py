import os
from dotenv import load_dotenv
import google.generativeai as genai
import chromadb
from embedder import Embedder
from lecture_parser import Parser

load_dotenv()

# check out pylance

class Storage:
    def __init__(self):
        self.db = chromadb.PersistentClient(
            path=os.getenv('LOCAL_DB_PATH')
        )

        self.lectures_tbl = self.db.get_or_create_collection(
            name="Lectures",
            # embedding_function=Embedder()
        )

        self.lessons_tbl = self.db.get_or_create_collection(
            name="Lessons",
        )


    def add_lesson(self, lesson, id):
        try:
            self.lessons_tbl.add(
                ids = [id],
                documents = [lesson['title']],
                metadatas=[lesson]
            )
            return True
        except Exception as e:
            print(e)
            return False

    def get_lessons(self):
        return self.lessons_tbl.get()['ids']

    def add_lecture(self, metadata, content, id):
        self.lectures_tbl.add(
            documents=[content], 
            ids=[id],
            metadatas=[metadata]
        )

    def query(self, query, **kwargs):
        embeddings = kwargs.get('embedding', None)
        n_results = kwargs.get('n_results', 10)
        filter = kwargs.get('where', None)
        filter_document = kwargs.get('where_document', None)
        data = kwargs.get('include', ["metadatas", "documents"])

        return self.lectures_tbl.query(
            query_embeddings = embeddings,
            n_results = n_results,
            where = filter,
            where_document = filter_document,
            query_texts = [query],
            include = data
        )
    
    def get_lectures(self, **kwargs):
        ids = kwargs.get('ids', None)
        where = kwargs.get('where', None)
        return self.lectures_tbl.get(
            ids = ids,
            where = where
        )




    