
import os
import google.generativeai as genai

# Get API key from environment (Render / local)
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_response(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        return "Thank you for your feedback."
    except Exception:
        # Never crash backend
        return "Thank you for your feedback. We appreciate you sharing your thoughts."
