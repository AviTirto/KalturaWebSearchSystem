import asyncio
from typing import List
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain_core.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from backend.utils.gemini_tools.gemini_types import SubQuestions, Selection, OCRResult

from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest", 
        temperature=0,
        safety_settings={HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE},
    )

def get_ocr_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0
    )

async def split_query_batch(llm, questions: List[str]):
    parser = PydanticOutputParser(pydantic_object=SubQuestions)
        
    prompt = PromptTemplate(
        template='''We are building a RAG search system where a user inputs in a question and then gets timestamps from lecture content
        best answering that question. Only if it makes the original question clearer, break down "{question}" into subquestions.
        Do not add any unrelated questions. If no subquestions are needed, then just use the original question.
        Don't make any repetitive questions. {format_instructions}''',
        input_variables=["question"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    formatted_questions = [prompt.format(question=q) for q in questions]
    
    results= llm.batch(
        formatted_questions
    )

    return [parser.parse(result.content) for result in results]

def format_subtitles(subtitles):
    output = ""
    for i, subtitle in enumerate(subtitles):
        output += f'\n{i}) {subtitle.subtitle}'
    return output

async def decide_subtitles_batch(llm, subtitles_list, questions: str):
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

    formatted_queries = [prompt.format(question=question, subtitles=format_subtitles(subtitles)) for question, subtitles in zip(questions, subtitles_list)]

    results= llm.batch(
        formatted_queries
    )

    return [parser.parse(result.content) for result in results]

async def ocr_batch(ocr_llm, images):
    parser = OutputFixingParser.from_llm(
        parser=PydanticOutputParser(pydantic_object=OCRResult),
        llm=ocr_llm
    )

    # Prepare the batch input
    formatted_queries = [
        [
            SystemMessage(
                content=(
                    "Extract text from this image into two PowerPoint slides. "
                    "There are two slides per page. Avoid graph text and ensure only content from the PowerPoint is included.\n\n"
                    "Return the output as a pure JSON object, without markdown formatting or code block syntax.\n"
                    f"{parser.get_format_instructions()}"
                )
            ),
            HumanMessage(
                content=[
                    {"type": "text", "text": "Extract text."}, 
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image}"}
                ]
            )
        ]
        for image in images
    ]

    # Use the batch function to process all images
    responses = ocr_llm.batch(formatted_queries)

    # Process each response
    results = []
    for response in responses:
        ocr_result = parser.parse(response.content)
        results.append({
            'result': ocr_result, 
            'input_tokens': response.usage_metadata['input_tokens'], 
            'output_tokens': response.usage_metadata['output_tokens']
        })

    return results


# asyncio batching

# async def decide_subtitles_batch(subtitles_batch: List[List[str]], question: str):
#     tasks = [decide_subtitles(subtitles, question) for subtitles in subtitles_batch]
#     results = await asyncio.gather(*tasks)
#     return results

# async def split_query_batch(questions: List[str]):
#     tasks = [split_query(question) for question in questions]
#     results = await asyncio.gather(*tasks)
#     return results

