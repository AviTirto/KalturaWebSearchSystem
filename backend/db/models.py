from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from pydantic import BaseModel

class Subtitles(BaseModel):  
    chunk_id: int
    index: int
    subtitle: str
    start_time: str
    end_time: str
    seconds: float
    lecture_id: int

    def get_chunk_id_as_str(self):
        return str(self.chunk_id)
    
    def get_lecture_id_as_str(self):
        return str(self.lecture_id)

class Lecture(BaseModel):
    lecture_id: int
    date: str
    title: str
    embed_link: str

    def get_lecture_id_as_str(self):
        return str(self.lecture_id)