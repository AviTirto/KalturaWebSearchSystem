from app.utils.gemini_tools.ppt_types import OCRResult
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
import json

class OCRModel:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0
        )

        self.parser = OutputFixingParser.from_llm(
            parser=PydanticOutputParser(pydantic_object=OCRResult),
            llm=self.model
        )

    def extract_text(self, image):
        response = self.model.invoke([
            SystemMessage(
                content=(
                    "Extract text from this image into two PowerPoint slides. "
                    "There are two slides per page. Avoid graph text and ensure only content from the PowerPoint is included.\n\n"
                    "Return the output as a pure JSON object, without markdown formatting or code block syntax.\n"
                    f"{self.parser.get_format_instructions()}"
                )
            ),
            HumanMessage(
                content=[
                    {"type": "text", "text": "Extract text."}, 
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image}"}
                ]
            )
        ])

        ocr_result = self.parser.parse(response.content)

        return {
            'result': ocr_result, 
            'input_tokens': response.usage_metadata['input_tokens'], 
            'output_tokens': response.usage_metadata['output_tokens']
        }
