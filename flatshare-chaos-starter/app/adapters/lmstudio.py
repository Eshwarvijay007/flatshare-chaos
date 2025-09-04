import os, httpx
from .base import LLMAdapter
class LMStudioAdapter(LLMAdapter):
    def __init__(self, model: str = None, base_url: str = None, api_key: str = None):
        self.model = model or os.getenv("LMSTUDIO_MODEL", "gpt-oss-20b")
        self.base_url = base_url or os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "not-needed")
        self.timeout = float(os.getenv("LMSTUDIO_TIMEOUT", "60"))
    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 128) -> str:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}]
        }
        with httpx.Client(timeout=self.timeout) as client:
            r = client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "").strip() or "(no content)"
