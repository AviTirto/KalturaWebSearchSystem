from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Subtitles(SQLModel, table=True):  # table=True indicates this is a database table
    chunk_id: Optional[str] = Field(default=None, primary_key=True)
    index: int
    subtitle: str
    start_time: str
    end_time: str
    seconds: float
    # This is the foreign key
    lecture_id: Optional[str] = Field(default=None, foreign_key="lecture.lecture_id")
    # Relationship to Lecture
    lecture: Optional["Lecture"] = Relationship(back_populates="subtitles")


class Lecture(SQLModel, table=True):
    lecture_id: Optional[str] = Field(default=None, primary_key=True)
    date: str
    title: str
    embed_link: str
    # Relationship to Subtitles
    subtitles: List[Subtitles] = Relationship(back_populates="lecture")
