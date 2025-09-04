import aiohttp
import asyncio
from .interface import Backend, Roast

class RealHTTPBackend(Backend):
    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout_s: int = 60):
        self.base_url = base_url
        self.timeout_s = timeout_s

    async def get_roasts(self, text, spice, characters):
        payload = {"text": text, "spice": spice, "characters": characters}
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout_s)) as sess:
            for attempt in range(3):
                try:
                    async with sess.post(f"{self.base_url}/roast", json=payload) as r:
                        r.raise_for_status()
                        data = await r.json()
                        return data["roasts"]
                except Exception:
                    if attempt == 2: raise
                    await asyncio.sleep(0.5 * (attempt + 1))
