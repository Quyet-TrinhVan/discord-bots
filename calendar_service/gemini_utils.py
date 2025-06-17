import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def extract_calendar_command(user_prompt: str) -> dict:
    system_prompt = """
        You are a smart assistant that specializes in analyzing schedules.
        Based on input, please, export to json includes:
        {
            "intent": "add_schedule" | "add_event" | "check_schedule" | "delete_event",
            "date": "YYYY-MM-DD", 
            "time": "HH:MM" | null,
            "title": "string" | null
        }
        If user says 'tomorrow' then convert to actual date (YYYY-MM-DD).
        If a field is not available, return null for that field.
        If the sentence is unrelated to calendar scheduling, return null.
    """
    response = model.generate_content([
        system_prompt,
        f"User: {user_prompt}"
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
    try:
        result = json.loads(text)
        return result
    except Exception as e:
        return None


