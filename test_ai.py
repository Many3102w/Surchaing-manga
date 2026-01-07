
import os
import google.generativeai as genai

API_KEY = os.environ.get('GEMINI_API_KEY')
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not set")
genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Hello")
    print(f"Success: {response.text}")
except Exception as e:
    print(f"Error: {e}")
