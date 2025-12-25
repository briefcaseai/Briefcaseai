-----------------------------------
| main.py                         |
-----------------------------------
| from fastapi import FastAPI     |
| from pydantic import BaseModel |
| from openai import OpenAI       |
|                                 |
| app = FastAPI()                |
| client = OpenAI()              |
|                                 |
| class InputData(BaseModel):    |
|     text: str                  |
|                                 |
@app.post("/generate")
def generate_documents(data: InputData):
    prompt = (
        "ROLE:\n"
        "You are an AI legal assistant generating internal law firm documents for attorneys.\n\n"
        "TASK:\n"
        "From the input text, generate TWO outputs exactly as structured below.\n\n"
        "OUTPUT 1 — CASE SUMMARY\n"
        "- Case title\n"
        "- Practice area\n"
        "- Parties involved\n"
        "- Timeline of events\n"
        "- Key facts\n"
        "- Potential legal issues (identify only; do NOT advise)\n"
        "- Missing or unclear information\n"
        "- Recommended internal next steps\n\n"
        "OUTPUT 2 — CLIENT INTAKE FORM\n"
        "- Client personal information\n"
        "- Incident or matter details\n"
        "- Dates and locations\n"
        "- Witnesses\n"
        "- Evidence available\n"
        "- Deadlines or time-sensitive items\n"
        "- Practice-area-specific intake questions\n\n"
        "RULES:\n"
        "- Neutral, factual, professional tone\n"
        "- Do NOT provide legal advice\n"
        "- Do NOT make assumptions beyond the provided text\n"
        "- Use clear headings and bullet points\n"
        "- Explicitly flag missing or unclear information\n"
        "- Assume U.S. law unless otherwise stated\n"
        "- Output must be suitable for internal law firm use\n\n"
        "INPUT:\n"
        f"{data.text}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"result": response.choices[0].message.content}
