from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()
client = OpenAI()

class InputData(BaseModel):
    data: dict  # accept full Tally payload

@app.post("/generate")
def generate_documents(data: InputData):

    # 1️⃣ Extract client notes from Tally fields
    client_text = ""

    fields = data.data.get("fields", [])
    for field in fields:
        if field.get("label") == "Paste client notes or case description":
            client_text = field.get("value", "")

    if not client_text:
        return {
            "output": "No client notes were received from the form."
        }

    # 2️⃣ Build prompt correctly (THIS FIXES THE SYNTAX ERROR)
    prompt = f"""
ROLE:
You are an AI legal assistant generating internal law firm documents for attorneys.

TASK:
From the input text, generate TWO outputs exactly as structured below.

OUTPUT 1 — CASE SUMMARY
- Case title
- Practice area
- Parties involved
- Timeline of events
- Key facts
- Potential legal issues (identify only; do NOT advise)
- Missing or unclear information
- Recommended internal next steps

OUTPUT 2 — CLIENT INTAKE FORM
- Client personal information
- Incident or matter details
- Dates and locations
- Witnesses
- Evidence available
- Deadlines or time-sensitive items
- Practice-area-specific intake questions

RULES:
- Neutral, factual, professional tone
- Do NOT provide legal advice
- Do NOT make assumptions beyond the provided text
- Use clear headings and bullet points
- Explicitly flag missing or unclear information
- Assume U.S. law unless otherwise stated
- Output must be suitable for internal law firm use

INPUT:
{client_text}
"""

    # 3️⃣ Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # 4️⃣ Return output for Tally
    return {
        "output": response.choices[0].message.content
    }

