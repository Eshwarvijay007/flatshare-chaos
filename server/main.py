# server/main.py
import os, time, asyncio, httpx
from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

CHAR_PROMPTS: Dict[str, str] = {
    "Corporate Carl": "You are Corporate Carl. KPI/OKR manager-speak. Roast crisply.",
    "Ghost Gina": "You are Ghost Gina. Non-committal, airy, vanishes. Roast gently but cutting.",
    "Party Pete": "You are Party Pete. High energy, chaotic, cheeky roasts.",
    "Prepper Priya": "You are Prepper Priya. Survivalist tough-love roasts."
}

class RoastReq(BaseModel):
    text: str
    spice: int = 2
    characters: List[str]

class RoastOut(BaseModel):
    character: str
    text: str
    score: float

class RoastResp(BaseModel):
    roasts: List[RoastOut]
    latency_ms: int

app = FastAPI(title="Flatshare Chaos Backend")

def build_prompt(sys: str, user_text: str, spice: int) -> str:
    return f"""{sys}

Rules:
- 1–2 sentences only.
- Roast (humorous jab), not harassment.
- Spice level: {spice} (0=mild … 5=spicy).
- No advice; only the roast.

User: {user_text}
Roast:"""

def score_roast(text: str, spice: int) -> float:
    t = (text or "").strip()
    if not t: return 0.0
    punc = sum(1 for c in t if c in "!?.")
    base = min(10.0, 3.0 + 0.02*len(t) + 0.8*punc)
    s = min(10.0, base + 0.6*spice)
    return round(s, 1)

async def ollama_generate(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{OLLAMA_URL}/api/generate", json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.9, "top_p": 0.9}
        })
        r.raise_for_status()
        data = r.json()
        text = (data.get("response") or "").strip()
        return text.split("\n")[0][:280]

@app.post("/roast", response_model=RoastResp)
async def roast(req: RoastReq):
    t0 = time.time()
    tasks = []
    for ch in req.characters:
        sys = CHAR_PROMPTS.get(ch, f"You are {ch}. Roast crisply; 1–2 sentences.")
        tasks.append(ollama_generate(build_prompt(sys, req.text, req.spice)))
    outs = await asyncio.gather(*tasks, return_exceptions=True)

    roasts: List[RoastOut] = []
    for ch, out in zip(req.characters, outs):
        text = "backend error, try again" if isinstance(out, Exception) else out
        roasts.append(RoastOut(character=ch, text=text, score=score_roast(text, req.spice)))

    return RoastResp(roasts=roasts, latency_ms=int((time.time()-t0)*1000))

@app.get("/health")
def health():
    return {"ok": True}
