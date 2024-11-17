from data_types import Chunk, Lesson
from typing import List
from db import Storage

storage = Storage() # remove the object-oriented DB
#  - Also add a relational database so that SQLAlchemy ORM can be added

def process_chunks(raw_chunks):
    lect_infos = raw_chunks['metadatas']
    subtitles = raw_chunks['documents']
    ids = raw_chunks['ids']

    processed_chunks = []

    for i in range(len(lect_infos)):
        processed_chunks+=[Chunk(
            ids[i],
            lect_infos[i]['index'],
            subtitles[i],
            lect_infos[i]['start_time'],
            lect_infos[i]['end_time'],
            lect_infos[i]['seconds'],
            lect_infos[i]['link']
        )]
    
    return processed_chunks


def queryLectures(query: str) -> Chunk:
    raw_chunks = storage.query(query)
    raw_chunks['metadatas'] = raw_chunks['metadatas'][0]
    raw_chunks['documents'] = raw_chunks['documents'][0]
    raw_chunks['ids'] = raw_chunks['ids'][0]
    return process_chunks(raw_chunks)
    

def get_chunk_by_id(**kwargs):
    id = kwargs.get('id', None)
    ids = kwargs.get('ids', [])
    if not id and not ids:
        raise 'ID or list of IDs must be provided'
    if id and ids:
        raise 'Either specify one of many IDs. A single ID and a list of IDs can not be processed'
    
    if id:
        raw_chunks = storage.get_lectures(
            ids = [id]
        )
        return process_chunks(raw_chunks)[0]
    else:
        raw_chunks = storage.get_lectures(
            ids = ids
        )
        return process_chunks(raw_chunks)


def get_chunks_by_link(link) -> List[Chunk]:
    raw_chunks = storage.get_lectures(
        where = {
            'link' : link
        }
    )

    return process_chunks(raw_chunks)


def get_lesson_by_link(link) -> Lesson:
    return storage.get_lessons(
        where = {
            'link' : link
        }
    )

