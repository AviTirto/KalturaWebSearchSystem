import os
import asyncio
from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from dotenv import load_dotenv
from validation_types import SubQuestions, Selection

# Global llm instance
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest", 
    temperature=0,
    safety_settings={HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE},
)

# Set API key and initialize llm
def set_key(key: str):
    os.environ['GOOGLE_API_KEY'] = key
    global llm
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest", 
        temperature=0,
        safety_settings={HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE},
    )

async def split_query(question: str):
    parser = PydanticOutputParser(pydantic_object=SubQuestions)
    
    prompt = PromptTemplate(
        template='''We are building a RAG search system where a user inputs in a question and then gets timestamps from lecture content
        best answering that question. Only if it makes the original question clearer, break down "{question}" into subquestions.
        Do not add any unrelated questions. If no subquestions are needed, then just use the original question.
        Don't make any repetitive questions. {format_instructions}''',
        input_variables=["question"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser
    result = await chain.ainvoke({"question": question})
    return result.subquestions

async def split_query_batch(questions: List[str]):
    tasks = [split_query(question) for question in questions]
    results = await asyncio.gather(*tasks)
    return results

async def summarizer(subtitles: List[str]):
    prompt = PromptTemplate(
        template="""The following is a set of summaries:
        {chunks}
        Take these and distill it into a final, consolidated summary
        of the main themes.""",
        input_variables=['chunks']
    )

    response = await llm.ainvoke(prompt.format(chunks=subtitles))
    return response.content

async def summarizer_batch(subtitles_batch: List[List[str]]):
    tasks = [summarizer(subtitles) for subtitles in subtitles_batch]
    results = await asyncio.gather(*tasks)
    return results

def format_subtitles(subtitles):
    output = ""
    for i, subtitle in enumerate(subtitles):
        output += f'\n{i}) {subtitle["content"]}'
    return output

async def decide_subtitles(subtitles, question: str):
    parser = PydanticOutputParser(pydantic_object=Selection)

    prompt = PromptTemplate(
        template='''You are a producer of a news station. Your job is to look at the subtitles of clips and select the ones that best answer the question: {question}.
        Only choose relevant ones. If none directly answer the question then don't return anything.
        Provide a short (maximum 100-word) explanation of why the subtitle answers the clip.
        Here are the following clips along with their associated id: {subtitles}
        {format_instructions}''',
        input_variables=["question", "subtitles"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser
    result = await chain.ainvoke({"question": question, "subtitles": format_subtitles(subtitles)})
    return result

async def decide_subtitles_batch(subtitles_batch: List[List[str]], question: str):
    tasks = [decide_subtitles(subtitles, question) for subtitles in subtitles_batch]
    results = await asyncio.gather(*tasks)
    return results

