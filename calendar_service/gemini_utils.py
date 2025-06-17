import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def extract_calendar_command(user_prompt: str) -> str:
    system_prompt = """
        You are a smart assistant that specializes in analyzing schedules from English.
        Based on input, please, export to json includes:
        {
            "intent": "add_schedule" | "add_event" | "check_schedule",
            "date": "YYYY-MM-DD", 
            "time": "HH:MM" | null,
            "title": "string" | null
        }
        If not enough information, return null.
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

# def _test_extract_calendar_command():
#     prompt1 = "Add a work schedule on 2025-06-18 at 09:00"
#     result1 = extract_calendar_command(prompt1)
#     print("Test 1:", result1)

#     prompt2 = "Create an event called Meeting on 2025-06-19 at 15:30"
#     result2 = extract_calendar_command(prompt2)
#     print("Test 2:", result2)

#     prompt3 = "What is my schedule for 2025-06-20?"
#     result3 = extract_calendar_command(prompt3)
#     print("Test 3:", result3)

#     prompt4 = "Remind me"
#     result4 = extract_calendar_command(prompt4)
#     print("Test 4:", result4)

# if __name__ == "__main__":
#     _test_extract_calendar_command()

