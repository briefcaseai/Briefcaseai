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
| @app.post("/generate")         |
| def generate_documents(...):   |
|     ...                         |
-----------------------------------
