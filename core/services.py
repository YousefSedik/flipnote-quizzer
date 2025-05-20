from django.conf import settings
from pydantic import BaseModel
from google import genai
import json
import fitz
import re


def get_content(uploaded_file) -> list[str]:
    content = []

    if uploaded_file.name.endswith(".pdf"):
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        if len(document) > 15:
            return "", False, "Max Value of pages is 15"
        for page in document:
            content.append(page.get_text())
        content = "".join(content)
    elif uploaded_file.name.endswith(".txt"):
        content = uploaded_file.readlines()
        content = "".join(content)
    else:
        return "", False, ".PDF or .TXT only are supported"
    return content, True, ""


class MCQ(BaseModel):
    text: str
    options: list[str]
    answer: str


class Written(BaseModel):
    text: str
    answer: str


class QuestionsModel(BaseModel):
    mcq: list[MCQ]
    written: list[Written]


def get_questions(content):
    prompt = f"""
You are given a document content. 
You need to extract and format it into 2 categories: written and mcq.
Document Content:
\"\"\"{content}\"\"\"
"""

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": QuestionsModel,
        },
    )
    response_text = response.text
    print(response_text)
    try:
        data: QuestionsModel = response.parsed
        return data.mcq, data.written
    except json.JSONDecodeError as e:
        print("JSON decode error:", str(e))
        return [], []
