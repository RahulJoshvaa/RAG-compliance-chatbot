
import google.generativeai as genai
from prompt_builder import build_prompt

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    GEMINI_MODEL
)

def generate(query) -> str:
    prompt = build_prompt(query)

    response = model.generate_content(
        prompt
    )

    return response.text