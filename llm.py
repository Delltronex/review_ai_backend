import google.generativeai as genai

# 🔴 SET YOUR API KEY HERE (LOCAL TESTING ONLY)
# API_KEY = "AIzaSyCFjHvD8Gt-qvPIKlM2fPy2IfHqmsii-xo"
API_KEY = "AIzaSyBTiDOstnVdkDnmYiHvJLJEHXoHNqLCqUU"

# Configure Gemini
genai.configure(api_key=API_KEY)

# Model
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_response(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        return "Thank you for your feedback."
    except Exception as e:
        # Never crash backend
        return "Thank you for your feedback. We appreciate you sharing your thoughts."
