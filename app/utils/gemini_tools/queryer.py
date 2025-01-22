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
from app.utils.gemini_tools.validation_types import SubQuestions, Selection
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from google.api_core import retry
import os
# Take in user query and break down the query into smaller queries using an LLM call


load_dotenv()
class Queryer():
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model = "gemini-1.5-flash-latest", 
            temperature=0,
            safety_settings={HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,})

    def set_key(self, key: str):
        os.environ['GOOGLE_API_KEY'] = key

        self.llm = ChatGoogleGenerativeAI(
            model = "gemini-1.5-flash-latest", 
            temperature=0,
            safety_settings={HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,})

    @retry.Retry(timeout=300.0)                   
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

        return chain.invoke({"question": question}).subquestions
    

    @retry.Retry(timeout=300.0)
    def summarizer(self, subtitles: List[str]):
        # Define prompt
        prompt = PromptTemplate(
            template="""
            The following is a set of summaries:
            {chunks}
            Take these and distill it into a final, consolidated summary
            of the main themes.
            """,
            input_variables=['chunks']
        )

        return self.llm.invoke(prompt.format(chunks=subtitles)).content
    
    def format_subtitles(self, subtitles):
        output = ""
        for i in range(len(subtitles)):
            output+=f'\n{i}) {subtitles[i]["content"]}'
        return output
    
    @retry.Retry(timeout=300.0)
    def decide_subtitles(self, subtitles, question: str):
        # Set up a parser + inject instructions into the prompt template.
        parser = PydanticOutputParser(pydantic_object=Selection)

        prompt = PromptTemplate(
            template='''
                You are a producer of a news station. Your job is to look at the subtitles of clips and select the ones that best answer the question: {question}.
                Only choose relevant ones. If none directly answer the question then don't return anything.
                Provide a short(maximum 100 word) explanation to why the subtitle answers the clip.
                Here are the following clips along with their associated id:
                {subtitles}
                {format_instructions}
            ''',
            input_variables=["question", "subtitles"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser

        return chain.invoke({"question": question, "subtitles": self.format_subtitles(subtitles)})
    


