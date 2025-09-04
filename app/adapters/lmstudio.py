import os
import httpx

class LMStudioAdapter:
    def __init__(self, base_url: str | None = None, model: str | None = None, timeout: int = 30):
        # Point to Ollama's OpenAI-compatible route instead of LM Studio's 1234
        self.base_url = base_url or os.getenv("OPENAI_BASE", "http://localhost:11434/v1")
        self.model = model or os.getenv("MODEL_NAME", "llama3.1")  # or llama3.1:latest if you pulled that tag
        self.timeout = timeout

    def generate(self, system_prompt: str, user_prompt: str, temperature: float, max_tokens: int) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            # No auth header needed for local Ollama; keep optional if you later proxy
        }
        payload = {
            "model": self.model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        with httpx.Client(timeout=self.timeout) as client:
            r = client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
