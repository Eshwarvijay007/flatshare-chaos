import re
try:
    import pyttsx3
except Exception:
    pyttsx3 = None

VOICE_MAP = {
    "Corporate Carl": "Alex",
    "Party Pete": "Samantha",
    "Ghost Gina": "Moira",
    "Lo-fi Luna": "Karen",
    "Prepper Priya": "Veena"
}

def list_voices():
    if not pyttsx3: 
        return []
    e = pyttsx3.init()
    return [(v.id, v.name) for v in e.getProperty("voices")]

def build_tts_engines(names):
    if not pyttsx3:
        raise RuntimeError("pyttsx3 not installed. pip install pyttsx3")
    engines = {}
    for name in names:
        eng = pyttsx3.init()
        chosen = None
        pref = VOICE_MAP.get(name)
        for v in eng.getProperty("voices"):
            if pref and pref.lower() in v.name.lower():
                chosen = v.id; break
        if chosen:
            eng.setProperty("voice", chosen)
        eng.setProperty("rate", 185)
        engines[name] = eng
    return engines
