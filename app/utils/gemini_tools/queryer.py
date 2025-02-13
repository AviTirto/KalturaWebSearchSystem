from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator
from langchain_google_genai import (
    AsyncChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from dotenv import load_dotenv
from app.utils.gemini_tools.validation_types import SubQuestions, Selection
import os
import asyncio

load_dotenv()

class Queryer():
    def __init__(self):
        self.llm = AsyncChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest", 
            temperature=0,
            safety_settings={HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,}
        )

    def set_key(self, key: str):
        os.environ['GOOGLE_API_KEY'] = key
        self.llm = AsyncChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest", 
            temperature=0,
            safety_settings={HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,}
        )

    async def split_query(self, question: str):
        parser = PydanticOutputParser(pydantic_object=SubQuestions)
        
        prompt = PromptTemplate(
            template='''
            We are building a RAG search system where a user inputs in a question and then gets timestamps from lecture content
            best answering that question.
            Only if it makes the original question clearer, break down "{question}" into subquestions.
            Do not add any unrelated questions.
            If no subquestions are needed, then just use the original question.
            Don't make any repetitive questions.
            {format_instructions}''',
            input_variables=["question"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser
        
        result = await chain.ainvoke({"question": question})
        return result.subquestions
    
    async def split_query_batch(self, questions: List[str]):
        # Create a list of coroutines for each question to split
        tasks = [self.split_query(question) for question in questions]
        # Use asyncio.gather to execute them concurrently
        results = await asyncio.gather(*tasks)
        return results

    async def summarizer(self, subtitles: List[str]):
        prompt = PromptTemplate(
            template="""
            The following is a set of summaries:
            {chunks}
            Take these and distill it into a final, consolidated summary
            of the main themes.
            """,
            input_variables=['chunks']
        )

        response = await self.llm.ainvoke(prompt.format(chunks=subtitles))
        return response.content
    
    async def summarizer_batch(self, subtitles_batch: List[List[str]]):
        # Create a list of coroutines for summarizing each batch of subtitles
        tasks = [self.summarizer(subtitles) for subtitles in subtitles_batch]
        # Execute the tasks concurrently
        results = await asyncio.gather(*tasks)
        return results
    
    def format_subtitles(self, subtitles):
        output = ""
        for i, subtitle in enumerate(subtitles):
            output += f'\n{i}) {subtitle["content"]}'
        return output
    
    async def decide_subtitles(self, subtitles, question: str):
        parser = PydanticOutputParser(pydantic_object=Selection)

        prompt = PromptTemplate(
            template='''
            You are a producer of a news station. Your job is to look at the subtitles of clips and select the ones that best answer the question: {question}.
            Only choose relevant ones. If none directly answer the question then don't return anything.
            Provide a short (maximum 100-word) explanation of why the subtitle answers the clip.
            Here are the following clips along with their associated id:
            {subtitles}
            {format_instructions}
            ''',
            input_variables=["question", "subtitles"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser
        result = await chain.ainvoke({"question": question, "subtitles": self.format_subtitles(subtitles)})
        return result
    
    async def decide_subtitles_batch(self, subtitles_batch: List[List[str]], question: str):
        # Create a list of coroutines for deciding subtitles for each batch
        tasks = [self.decide_subtitles(subtitles, question) for subtitles in subtitles_batch]
        # Execute the tasks concurrently
        results = await asyncio.gather(*tasks)
        return results