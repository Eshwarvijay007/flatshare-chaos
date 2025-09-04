from abc import ABC, abstractmethod
class LLMAdapter(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 128) -> str:
        raise NotImplementedError
