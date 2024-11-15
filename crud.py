from data_types import Chunk, Lesson
from db import Storage

storage = Storage() # remove the object-oriented DB
#  - Also add a relational database so that SQLAlchemy ORM can be added

def queryLectures(query: str) -> Chunk:
    raw_chunks = storage.query(query)
    lect_infos = raw_chunks['metadatas'][0]
    subtitles = raw_chunks['documents'][0]
    ids = raw_chunks['ids'][0]

    processed_chunks = []

    for i in range(len(lect_infos)):
        processed_chunks+=[Chunk(
            ids[i],
            lect_infos[i]['index'],
            subtitles[i],
            lect_infos[i]['start_time'],
            lect_infos[i]['end_time'],
            lect_infos[i]['seconds'],
            lect_infos[i]['lecture_link']
        )]
    
    return processed_chunks

def get_chunk_by_id(self, id):
    pass

def get_chunks_by_link(self, link) -> [Chunk]: