# app/adapters/ollama_streaming.py
import os, json
import httpx
from typing import Iterator

class OllamaStreamingAdapter:
    def __init__(self, base_url: str | None = None, model: str | None = None, timeout: int = 60):
        self.base_url = base_url or os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
        self.model = model or os.getenv("MODEL_NAME", "gpt-oss:20b")
        self.timeout = timeout

    def _prompt(self, system_prompt: str, user_prompt: str) -> str:
        # Simple merged prompt; works fine for short, crisp outputs
        return f"{system_prompt}\n\n{user_prompt}"

    def generate_stream(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 128,
    ) -> Iterator[str]:
        """
        Yields incremental text chunks as they arrive from Ollama.
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": self._prompt(system_prompt, user_prompt),
            "stream": True,
            "options": {"temperature": temperature},
        }
        with httpx.Client(timeout=self.timeout) as client:
            with client.stream("POST", url, json=payload) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line:
                        continue
                    # Each line is a JSON object like: {"model":"...","created_at":"...","response":"chunk","done":false}
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    chunk = obj.get("response", "")
                    if chunk:
                        yield chunk
                    if obj.get("done"):
                        break

    # Backward-compatible "full" call if you need it anywhere
    def generate(self, system_prompt, user_prompt, temperature=0.7, max_tokens=128) -> str:
        return "".join(self.generate_stream(system_prompt, user_prompt, temperature, max_tokens))
