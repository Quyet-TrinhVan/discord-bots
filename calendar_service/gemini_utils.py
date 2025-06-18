import google.generativeai as genai
import os
import json
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def replace_relative_dates(prompt: str) -> str:
    today = datetime.now().date()
    replacements = {
        "tomorrow": str(today + timedelta(days=1)),
        "today": str(today)
    }
    for word, actual in replacements.items():
        prompt = re.sub(rf"\b{word}\b", actual, prompt, flags=re.IGNORECASE)
    return prompt

def extract_calendar_command(user_prompt: str) -> dict:
    system_prompt = """
        You are a smart assistant that specializes in analyzing schedules.
        Based on input, please, export to json includes:
        {
            "intent": "add_event" | "check_schedule" | "delete_event" | "update_event",
            "date": "YYYY-MM-DD", 
            "time": "HH:MM" | null,
            "title": "string" | null,
        }
        If a field is not available, return null for that field.
        If the sentence is unrelated to calendar scheduling, return null.
    """

    prompt_text = replace_relative_dates(user_prompt)

    response = model.generate_content([
        system_prompt,
        f"User: {prompt_text}"
    ])

    text = getattr(response, 'text', None)
    if text is None:
        return None

    if text.startswith('```json'):
        text = text.lstrip('`').lstrip('json').strip()
    if text.startswith('```'):
        text = text.lstrip('`').strip()
    if text.endswith('```'):
        text = text[:-3].strip()

    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None

    try:
        result = json.loads(match.group())
        return result
    except json.JSONDecodeError:
        return None