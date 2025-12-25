from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/generate", response_class=HTMLResponse)
async def generate_get():
    return """
    <html>
      <body style="font-family: Arial; padding: 40px;">
        <h2>Backend is live</h2>
        <p>Submit the form to generate documents.</p>
      </body>
    </html>
    """

@app.post("/generate")
async def generate_post(request: Request):
    payload = await request.json()
    return payload

