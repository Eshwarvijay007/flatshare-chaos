import re
PROTECTED = re.compile(r"\b(race|religion|gender|sexual|disab|ethnic|caste)\b", re.IGNORECASE)
SLUR = re.compile(r"\b(\w*slur\w*)\b", re.IGNORECASE)
def sanitize_roast(text: str) -> str:
    if PROTECTED.search(text) or SLUR.search(text):
        return "Let's keep it classy—PG-13 roast only."
    return text.strip()[:200]
