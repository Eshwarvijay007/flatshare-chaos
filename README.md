# Flatshare Chaos: Roast Edition (macOS, offline-first)

An offline multi-agent roommate simulator where distinct AI roommates roast you and each other.
Runs locally; supports text-only or voice I/O on macOS.

## Quickstart (Text-only)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.ui.cli --backend=real
```

## Voice I/O (macOS, offline)
1) Install extra voices (System Settings → Accessibility → Spoken Content → Manage Voices…)
2) List voices: `say -v '?'`
3) Install audio libs:
```bash
pip install pyttsx3 sounddevice vosk
```
4) Download a small Vosk English model and put it under `models/vosk-en-small/`.

Run:
```bash
python -m app.ui.cli --backend=mock --voice --mic --vosk-model models/vosk-en-small
```

## LM Studio backend (optional, real LLM)
```bash
export OPENAI_API_BASE=http://localhost:1234/v1
export OPENAI_API_KEY=not-needed
python -m app.ui.cli --backend=lmstudio --spice=2
```

