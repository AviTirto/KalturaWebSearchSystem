
from app.models.ChromaModel.cdb import Storage
from app.services.lecture_manager import generate_unique_chunk_id
from app.utils.gemini_tools.queryer import Queryer
from app.utils.database_tools.crud import CRUDManager
from typing import List
from sqlmodel import Session

class QueryManager():
    def __init__(self, session : Session):
        self.db = Storage()
        self.queryer = Queryer()
        self.crud_manager = CRUDManager(session, self.db)

    def set_key(self, key: str):
        self.queryer.set_key(key)

    # This should just take in a list of Subtitle objects and remove the duplicates
    def remove_duplicate_chunks(self, subtitle_chunks):
        uuids = set()
        unique_chunks = []

        for chunk in subtitle_chunks:

            if chunk.chunk_id in uuids:
                continue
            uuids.add(chunk.chunk_id)
            unique_chunks.append(chunk)

        return unique_chunks

    def get_neighbors(self, subtitle_chunk):
        chunk_index = subtitle_chunk.index
        lecture_id = subtitle_chunk.lecture_id
        lecture_subtitles = self.crud_manager.get_all_subtitles_by_lecture(lecture_id)
        lecture_subtitles.sort(key=lambda s: s.index)

        current_index = next((i for i, subtitle in enumerate(lecture_subtitles) if subtitle.index == chunk_index), None)
        if current_index is None:
            raise ValueError(f"Chunk with index {chunk_index} not found for lecture_id {lecture_id}")

        start_index = max(0, current_index - 2)
        end_index = min(len(lecture_subtitles), current_index + 3)

        neighboring_subtitles = lecture_subtitles[start_index:end_index]
        return neighboring_subtitles


    def summarize_chunks(self, chunks):
        start_time = chunks[0].start_time
        end_time = chunks[-1].end_time
        seconds = chunks[0].seconds
        lecture_id = chunks[0].lecture_id
        
        combined_subtitle = "\n".join([chunk.subtitle for chunk in chunks])
        summary = self.queryer.summarizer(combined_subtitle)

        # Should possibly change this? Make this a Subtitile? 
        return {"content" : summary, "start_time": start_time, "end_time" : end_time, "seconds":seconds, "lecture_id" : lecture_id}



    def query(self, input: str):
        subquestions = self.queryer.split_query(input)
        subtitle_chunks_list = []
        for question in subquestions:
            subtitle_chunks = self.crud_manager.query_lectures(question)
            subtitle_chunks_list.append(subtitle_chunks)

        #print(subtitle_chunks_list)
        subtitle_chunks_list = subtitle_chunks_list[0]
        unique_chunks = self.remove_duplicate_chunks(subtitle_chunks_list)
        summaries = []

        for chunk in unique_chunks:
            neighbors = self.get_neighbors(chunk)
            summaries += [self.summarize_chunks(neighbors)]

        indexes = self.queryer.decide_subtitles(summaries, input)
        return [summaries[i] for i in indexes]


