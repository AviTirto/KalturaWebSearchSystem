from typing import List
from pydantic import BaseModel

# Define Pydantic models
class Answer(BaseModel):
    content: str  # content of answer
    question_id: str  # question id
    answer_id: str  # answer id
    created: str  # date created
    tag: int  # 0 denotes instructor endorsement, 1 denotes instructor answer

class Question(BaseModel):
    content: str  # content of question
    question_id: str  # question id
    created: str  # date created

class Post(BaseModel):
    question: Question  # question object
    answers: List[Answer]  # list of answers