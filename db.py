import os
from dotenv import load_dotenv
import google.generativeai as genai
import chromadb
from embedder import Embedder
from lecture_parser import Parser

load_dotenv()

class Storage:
    def __init__(self):
        self.db = chromadb.PersistentClient(
            path=os.getenv('LOCAL_DB_PATH')
        )

        self.lectures_tbl = self.db.get_or_create_collection(
            name="Lectures",
            embedding_function=Embedder()
        )

        self.parser = Parser()

    def add_lecture(self, lecture_path: str):
        chunks = self.parser.parse_chunks(lecture_path)
 
        for index, chunk in enumerate(chunks):
            content = chunk['content']
            start_time = chunk['start_time']
            end_time = chunk['end_time']
            seconds = chunk['seconds']

            print("INDEX", index)

            self.lectures_tbl.add(
                documents=[content], 
                ids=[str(index)],
                metadatas=[{
                    "lecture":lecture_path,
                    "start_time": start_time,
                    "end_time": end_time,
                    "seconds": seconds
                }]
            )



    