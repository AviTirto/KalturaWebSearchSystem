from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator


# Define your desired data structure.
class SubQuestions(BaseModel):
    subquestions: List[str] = Field(description="One or more questions")


    
    


