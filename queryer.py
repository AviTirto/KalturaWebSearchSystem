from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from dotenv import load_dotenv
from validation_types import SubQuestions
# Take in user query and break down the query into smaller queries using an LLM call


load_dotenv()
class Queryer():
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model = "gemini-1.5-flash-latest", 
            temperature=0,
            safety_settings={HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,})

                             
    def split_query(self, question):
        # Set up a parser + inject instructions into the prompt template.
        parser = PydanticOutputParser(pydantic_object=SubQuestions)

        prompt = PromptTemplate(
            template='''
            We are building a RAG search system where a user inputs in a question and then gets timestamps from lecture content
            best anserwing that question.
            Only if it makes the original question clearer, break down "{question}" into subquestions.
            Do not add any unrelated questions.
            If no subquestions are needed, then just use the original question.
            Dont make any repetitive questions.
            {format_instructions}''',
            input_variables=["question"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser

        return chain.invoke({"question": question})
    


