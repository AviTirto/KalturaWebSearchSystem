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

    def query(self, query):
        results = self.lectures_tbl.query(
            query_texts = [query],
            n_results = 10
        )
        return [doc[0] for doc in results['documents']]



    