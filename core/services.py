from django.conf import settings
from google import genai
import json
import fitz


def get_content(uploaded_file) -> list[str]:
    content = []

    if uploaded_file.name.endswith(".pdf"):
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in document:
            content.append(page.get_text())
        content = "".join(content)
        print(content)
    elif uploaded_file.name.endswith(".txt"):
        print(dir(uploaded_file))
        content = uploaded_file.readlines()
        content = "".join(content)
    else:
        return "", False, ".PDF or .TXT only are supported"
    return content, True, ""


def get_questions(content):
    prompt = f"""
You are given a document content. 
You need to extract and format it into 2 categories: written and mcq.

Document Content:
\"\"\"{content}\"\"\"

Output Format (JSON):
{{
  "mcq": [
    {{
      "text": "What is ...?",
      "options": ["A", "B", "C", "D"],
      "answer": "A"
    }},
    ...
  ],
  "written": [
    {{
      "text": "Explain the concept of ...",
      "answer": "..."
    }},
    ...
  ]
}}
"""
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
    response_text = response.text
    try:
        data = json.loads(response_text)
        return data.get("mcq"), data.get("written")
    except json.JSONDecodeError as e:
        return {}, {}
