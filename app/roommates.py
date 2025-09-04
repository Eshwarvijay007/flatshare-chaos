from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Roommate:
    name: str
    style: str
    roast_signature: str
    quirks: List[str]
    triggers: Dict[str, List[str]]
    spice: int = 2
    roast_count: int = 0
    memory: List[str] = field(default_factory=list)
