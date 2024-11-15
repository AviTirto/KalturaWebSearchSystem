
from db import Storage
from lecture_manager import generate_unique_id
from queryer import Queryer
from crud import queryLectures, get_chunk_by_id, get_chunks_by_link
from typing import List
from data_types import Chunk

class QueryManager():
    def __init__(self):
        self.db = Storage()
        self.queryer = Queryer()

    def remove_duplicate_chunks(self, chunks: List[Chunk]) -> List[Chunk]:
        
        uuids = set()
        unique_chunks = []

        for i in range(len(chunks)):
            if chunks[i].id in uuids:
                continue

            uuids.add(chunks[i].id)
            unique_chunks += [chunks[i]]

        return unique_chunks


    def get_neighbors(self, chunk: Chunk) -> List[Chunk]:
        n_chunks = len(get_chunks_by_link(chunk.link))

        ids = [generate_unique_id(chunk.link, i) for i in range(max(chunk.index - 2, 0), min(chunk.index + 3, n_chunks))]
        
        return get_chunk_by_id(ids)

    

    def summarize_chunks(self, chunks):
        start_time = chunks[0].start_time
        


    def query(self, input: str):
        subquestions = self.queryer.split_query(input)

        for question in subquestions:
            chunks = queryLectures(question)


        unique_chunks = self.remove_duplicate_chunks(chunks)

        for chunk in unique_chunks:
            self.get_neighbors(chunk)


