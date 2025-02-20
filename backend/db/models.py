from typing import List, Optional
from pydantic import BaseModel

class Subtitle(BaseModel):  
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
    
class Slide(BaseModel):  
    slide_id: int
    page_num: int
    text: str
    ppt_id: int

    def get_slide_id_as_str(self):
        return str(self.slide_id)
    
    def get_ppt_id_as_str(self):
        return str(self.ppt_id)
    
class PPT(BaseModel):
    ppt_id: int
    title: str
    path: str

    def get_ppt_id_as_str(self):
        return str(self.ppt_id)
    
