from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "samantha-mistral"

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    response = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt}, stream=True)
    text = ""
    for line in response.iter_lines():
        if line:
            try:
                decoded = line.decode("utf-8")
                if '"response":"' in decoded:
                    part = decoded.split('"response":"')[1].split('"')[0]
                    text += part
            except Exception:
                pass

    return {"reply": text}
