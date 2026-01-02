# from fastapi import FastAPI
# from pydantic import BaseModel
# import pandas as pd
# from datetime import datetime
# from llm import generate_response
# import os

# app = FastAPI()

# DATA_FILE = "feedback.csv"

# if not os.path.exists(DATA_FILE):
#     df = pd.DataFrame(columns=[
#         "timestamp",
#         "rating",
#         "review",
#         "ai_response",
#         "summary",
#         "recommended_action"
#     ])
#     df.to_csv(DATA_FILE, index=False)

# class Feedback(BaseModel):
#     rating: int
#     review: str

# @app.post("/submit")
# def submit_feedback(data: Feedback):
#     user_prompt = f"""
#     User rated {data.rating}/5 and wrote:
#     "{data.review}"

#     Write a polite, friendly response in 2 sentences.
#     """

#     summary_prompt = f"Summarize this review in one short sentence:\n{data.review}"
#     action_prompt = f"Suggest one improvement action based on this review:\n{data.review}"

#     ai_response = generate_response(user_prompt)
#     summary = generate_response(summary_prompt)
#     action = generate_response(action_prompt)

#     row = {
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "rating": data.rating,
#         "review": data.review,
#         "ai_response": ai_response,
#         "summary": summary,
#         "recommended_action": action
#     }

#     df = pd.read_csv(DATA_FILE)
#     df = pd.concat([df, pd.DataFrame([row])])
#     df.to_csv(DATA_FILE, index=False)

#     return {"ai_response": ai_response}

# @app.get("/feedback")
# def get_feedback():
#     df = pd.read_csv(DATA_FILE)
#     return df.to_dict(orient="records")


from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from datetime import datetime
from llm import generate_response
import os

app = FastAPI()

# =========================
# CORS CONFIG
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://review-ai-user.vercel.app/",
        "https://review-ai-admin.vercel.app/"
        
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DATA FILE
# =========================
DATA_FILE = "feedback.csv"

COLUMNS = [
    "timestamp",
    "rating",
    "review",
    "ai_response",
    "summary",
    "recommended_action",
]

# =========================
# ENSURE CSV EXISTS & VALID
# =========================
def ensure_csv():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATA_FILE, index=False)

ensure_csv()

# =========================
# SCHEMA
# =========================
class Feedback(BaseModel):
    rating: int
    review: str

# =========================
# SUBMIT FEEDBACK
# =========================
@app.post("/submit")
def submit_feedback(data: Feedback):
    ensure_csv()

    user_prompt = f"""
    User rated {data.rating}/5 and wrote:
    "{data.review}"

    Write a polite, friendly response in 2 sentences.
    """

    summary_prompt = f"Summarize this review in one short sentence:\n{data.review}"
    action_prompt = f"Suggest one improvement action based on this review:\n{data.review}"

    ai_response = generate_response(user_prompt)
    summary = generate_response(summary_prompt)
    action = generate_response(action_prompt)

    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rating": data.rating,
        "review": data.review,
        "ai_response": ai_response or "",
        "summary": summary or "",
        "recommended_action": action or "",
    }

    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    return {"ai_response": ai_response}

# =========================

# =========================
@app.get("/feedback")
def get_feedback():
    ensure_csv()

    try:
        df = pd.read_csv(DATA_FILE)
    except Exception:
        return []

    # ✅ VERY IMPORTANT: make JSON safe
    df = df.replace([float("inf"), float("-inf")], "")
    df = df.fillna("")

    return df.to_dict(orient="records")



