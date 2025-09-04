from typing import List, TypedDict

class Roast(TypedDict):
    character: str
    text: str
    score: float

class Backend:
    async def get_roasts(self, text: str, spice: int, characters: List[str]) -> List[Roast]:
        raise NotImplementedError
