from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from openai import OpenAI

app = FastAPI()
client = OpenAI()

@app.get("/generate", response_class=HTMLResponse)
async def generate_get():
    return """
    <html>
      <body style="font-family: Arial; padding: 40px;">
        <h2>No case data received</h2>
        <p>Please submit the form to generate documents.</p>
      </body>
    </html>
    """

@app.post("/generate", response_class=HTMLResponse)
async def generate_post(request: Request):
    payload = await request.json()

    fields = payload.get("data", {}).get("fields", [])
    client_text = ""

    for field in fields:
        if "Paste client notes" in field.get("label", ""):
            client_text = field.get("value", "")

    if not client_text:
        client_text = "No client notes provided."

    prompt = f"""
You are an AI legal assistant generating internal law firm documents.

Generate:
1) CASE SUMMARY
2) CLIENT INTAKE FORM

INPUT:
{client_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response.choices[0].message.content

    return f"""
    <html>
      <head>
        <title>AI Case Summary</title>
        <style>
          body {{
            font-family: Arial, sans-serif;
            padding: 40px;
            max-width: 900px;
            margin: auto;
            white-space: pre-wrap;
          }}
        </style>
      </head>
      <body>
        <h1>AI-Generated Case Summary & Intake</h1>
        <pre>{output}</pre>
      </body>
    </html>
    """
