from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator


# Define your desired data structure.
class SubQuestions(BaseModel):
    subquestions: List[str] = Field(description="One or more questions")

class Selection(BaseModel):
    indexes: List[int] = Field(description="The indexes of the subtitles")
    reasons: List[str] = Field(description="Reason why the subtitles answer the question")
    
    
