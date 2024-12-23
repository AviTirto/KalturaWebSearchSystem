from typing import List, Dict, Any
from sqlmodel import Session, select
from app.models.ChromaModel.cdb import Storage
from app.models.SQLModel.models import Subtitles, Lecture


class CRUDManager:
    def __init__(self, session: Session, storage: Storage):
        """
        Initialize the CRUDManager with a database session and storage service.
        :param session: A SQLModel session instance.
        :param storage: A Storage instance for vector search operations.
        """
        self.session = session
        self.storage = storage

    def get_all_lecture_ids(self) -> List[int]:
        """
        Retrieve all lecture IDs from the database.
        :return: A list of lecture IDs.
        """
        statement = select(Lecture.lecture_id)
        results = self.session.exec(statement).all()
        return [lecture_id for lecture_id in results if lecture_id is not None]
    
    def get_all_lecture_titles(self) -> List[str]:
        statement = select(Lecture.title)
        results = self.session.exec(statement).all()
        return results
    
    def delete_all_lectures(self):
        statement = select(Lecture)
        lectures = self.session.exec(statement).all()
        for lecture in lectures:
            self.session.delete(lecture)
        self.session.commit()

    def get_lecture_metadata(self, lecture_id: int) -> Lecture:
        """
        Retrieve metadata for a specific lecture.
        :param lecture_id: The ID of the lecture to retrieve.
        :return: The Lecture object or raises an error if not found.
        """
        statement = select(Lecture).where(Lecture.lecture_id == lecture_id)
        lecture_obj = self.session.exec(statement).first()
        if not lecture_obj:
            raise ValueError(f"No lecture found for lecture_id {lecture_id}")
        return lecture_obj

    def add_lecture_metadata(self, lecture_data: Dict[str, Any]) -> Lecture:
        """
        Add a new lecture to the database.
        :param lecture_data: A dictionary containing the lecture metadata.
        :return: The newly created Lecture object.
        """
        lecture = Lecture(**lecture_data)
        self.session.add(lecture)
        self.session.commit()
        self.session.refresh(lecture)
        return lecture

    def add_subtitle_metadata(self, subtitle_data: Dict[str, Any]) -> Subtitles:
        """
        Add a new subtitle to the database.
        :param subtitle_data: A dictionary containing the subtitle metadata.
        :return: The newly created Subtitles object.
        """
        subtitle = Subtitles(**subtitle_data)
        self.session.add(subtitle)
        self.session.commit()
        self.session.refresh(subtitle)
        return subtitle

    def get_subtitle_metadata(self, chunk_id: str) -> Subtitles:
        """
        Retrieve metadata for a specific subtitle chunk.
        :param chunk_id: The ID of the subtitle chunk to retrieve.
        :return: The Subtitles object or raises an error if not found.
        """
        statement = select(Subtitles).where(Subtitles.chunk_id == chunk_id)
        subtitle_obj = self.session.exec(statement).first()
        if not subtitle_obj:
            raise ValueError(f"No subtitle found for chunk_id {chunk_id}")
        return subtitle_obj

    def query_lectures(self, query: str) -> List[Subtitles]:
        """
        Perform a vector search on the database and retrieve metadata for the matching chunks.
        :param query: The query string to search for.
        :return: A list of Subtitles objects for the matching chunks.
        """
        raw_chunks = self.storage.vector_search(query)
        if not raw_chunks or 'ids' not in raw_chunks:
            raise ValueError("No matching chunks found.")

        subtitle_obj_list = []
        for chunk_id in raw_chunks['ids'][0]:
            subtitle_obj = self.get_subtitle_metadata(chunk_id)
            subtitle_obj_list.append(subtitle_obj)

        
        return subtitle_obj_list

    def get_all_subtitles_by_lecture(self, lecture_id: int) -> List[Subtitles]:
        """
        Retrieve all subtitle chunks for a specific lecture.
        :param lecture_id: The ID of the lecture to retrieve subtitles for.
        :return: A list of Subtitles objects.
        """
        statement = select(Subtitles).where(Subtitles.lecture_id == lecture_id)
        subtitles = self.session.exec(statement).all()
        if not subtitles:
            raise ValueError(f"No subtitles found for lecture_id {lecture_id}")
        return subtitles