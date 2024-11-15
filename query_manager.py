from db import Storage
from lecture_manager import generate_unique_id
from queryer import Queryer
from crud import queryLectures
from data_types import Chunk

class QueryManager():
    def __init__(self):
        self.db = Storage()
        self.queryer = Queryer()

    def remove_duplicate_chunks(self, chunks):
        
        uuids = set()
        unique_chunks = []

        for i in range(len(chunks)):
            if chunks[i].id in uuids:
                continue

            uuids.add(chunks[i].id)
            unique_chunks += [chunks[i]]

        return unique_chunks


    def get_neighbors(self, lect_info):
        index = lect_info['index']
        link = lect_info['link']

        n_chunks = len(
            self.db.get_lectures(
                where = {
                    'link' : link
                }
            )['metadatas']
        )

        ids = [generate_unique_id(link, i) for i in range(max(index - 2, 0), min(index + 3, n_chunks))]
        
        neighbors = self.db.get_lectures(
            ids = ids
        )

        n_lect_infos = neighbors['metadatas']
        n_docs = neighbors['documents']

        return {
            'lect_info': n_lect_infos,
            'docs': n_docs
        }
    

    def summarize_chunks(self, chunks):
        pass


    def query(self, input: str):
        subquestions = self.queryer.split_query(input)

        for question in subquestions:
            chunks = queryLectures(question)

        unique_chunks = self.remove_duplicate_chunks(chunks)


