from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # змінити на конкретні домени, якщо потрібно
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "samantha-mistral"

system_prompt = """
Тебе звати Chet Gipeeti.

Ти — професійний психолог і співрозмовник, який уважно слухає, не оцінює, і допомагає людині зрозуміти власні почуття.  
Твоя мета — створити спокійну, довірливу атмосферу.  
Ти відповідаєш українською мовою, доброзичливо і розуміюче.  
...
"""

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    full_prompt = f"### System:\n{system_prompt}\n### User:\n{prompt}\n### Assistant:"

    try:
        response = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": full_prompt}, stream=True)
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection to Ollama failed: {e}"}

    if response.status_code != 200:
        return {"error": f"Ollama error: {response.status_code}"}

    text = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line)
                if "response" in data:
                    text += data["response"]
            except json.JSONDecodeError:
                continue

    return {"reply": text}
