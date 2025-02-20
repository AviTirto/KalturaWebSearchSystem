from typing import List, Optional
from pydantic import BaseModel, Field

# Define your desired data structure.
class SubQuestions(BaseModel):
    subquestions: List[str] = Field(description="One or more questions")

class Selection(BaseModel):
    indexes: List[int] = Field(description="The indexes of the subtitles")
    reasons: List[str] = Field(description="Reason why the subtitles answer the question")

class OCRResult(BaseModel):
    slide_1_text: str = Field(description="Text from slide 1.")
    slide_2_text: Optional[str] = Field(default = None, description="Text from slide 2. If there are two slides. If not then None.")
    
    
