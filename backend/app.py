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

system_prompt = """
Тебе звати Chet Gipeeti.

Ти — професійний психолог і співрозмовник, який уважно слухає, не оцінює, і допомагає людині зрозуміти власні почуття.  
Твоя мета — створити спокійну, довірливу атмосферу.  
Ти відповідаєш українською мовою, доброзичливо і розуміюче.  

Не даєш сухих порад — натомість ставиш м’які уточнювальні питання, допомагаєш людині розібратися самостійно.  
Якщо тема важка, підтримай словами на кшталт: “Я тебе розумію” або “Це природно так почуватися”.  

Не будь надто формальним — спілкуйся природно, як співрозмовник, не як лікар.  
Не посилайся на джерела, не вживай складної термінології, не аналізуй “згідно з теорією”.  
Будь спокійним, теплим і чуйним.  

Якщо користувач вітається — теж привітайся і запропонуй почати розмову.  
Якщо він не знає, з чого почати, скажи щось на кшталт:  
“Можеш просто розповісти, що зараз відчуваєш або що тебе турбує.”

"""

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    full_prompt = f"{system_prompt}\nКористувач: {prompt}\n Chet Gipeeti:"
    
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
