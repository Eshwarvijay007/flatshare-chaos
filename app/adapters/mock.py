import random
from .base import LLMAdapter
GENERIC = [
    "Noted. Consider a reset and over-index on consistency.",
    "Your execution needs fewer excuses and more momentum.",
    "Chore governance is failing—launch DishOps.",
    "Rent is a constraint, not an excuse.",
    "That idea had less life than my cactus.",
    "Even your excuses are underperforming KPIs.",
    "Party Pete thinks you need shots, not strategies.",
    "Ghost Gina saw more spirit in an empty room.",
]

class MockAdapter(LLMAdapter):
    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 128) -> str:
        return random.choice(GENERIC)
