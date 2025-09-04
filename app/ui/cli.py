# app/ui/cli.py
from __future__ import annotations

import argparse
import sys
from typing import Tuple, List, Any
from rich.console import Console

# Engine
from app.engine import Engine

# Adapters
try:
    from app.adapters.ollama_streaming import OllamaStreamingAdapter  # streaming provider
except Exception:
    OllamaStreamingAdapter = None  # type: ignore

try:
    from app.adapters.lmstudio import LMStudioAdapter  # non-stream (OpenAI-compat)
except Exception:
    LMStudioAdapter = None  # type: ignore

console = Console()


def parse_spoken_line(line: str) -> Tuple[str | None, str | None]:
    """Split 'Name: text' → (Name, text). Returns (None, None) if not matched."""
    if not isinstance(line, str) or ":" not in line:
        return None, None
    who, text = line.split(":", 1)
    who, text = who.strip(), text.strip()
    if not who or not text:
        return None, None
    return who, text


def _load_roommates_module() -> Any | None:
    """
    Try to import roommates module from multiple locations:
      1) app.roommates  (repo_root/app/roommates.py)
      2) roommates      (repo_root/roommates.py)
    Return the module or None.
    """
    # Try app.roommates
    try:
        from app import roommates as rm  # type: ignore
        return rm
    except Exception:
        pass
    # Try top-level roommates
    try:
        import roommates as rm  # type: ignore
        return rm
    except Exception:
        return None


def load_roommates() -> List[object]:
    """
    Load roommates robustly:
      - Prefer ROOMMATES from roommates module
      - Else try factory functions
      - Else build inline defaults with a simple compatible class
    """
    rm = _load_roommates_module()

    # 1) Use provided list if present and non-empty
    if rm is not None and hasattr(rm, "ROOMMATES"):
        try:
            lst = getattr(rm, "ROOMMATES")
            if isinstance(lst, list) and len(lst) > 0:
                return lst
        except Exception:
            pass

    # 2) Try factory functions if defined
    if rm is not None:
        for fn_name in ("default_roommates", "make_roommates", "build_roommates"):
            if hasattr(rm, fn_name):
                fn = getattr(rm, fn_name)
                try:
                    lst = fn()
                    if isinstance(lst, list) and len(lst) > 0:
                        return lst
                except Exception:
                    pass

    # 3) Build inline defaults. If roommates.Roommate exists, use it; else use a simple fallback class.
    if rm is not None and hasattr(rm, "Roommate"):
        R = getattr(rm, "Roommate")
    else:
        # Minimal attribute-compatible fallback
        class R:  # noqa: N801
            def __init__(self, name, style, roast_signature, quirks=None, triggers=None, spice=2):
                self.name = name
                self.style = style
                self.roast_signature = roast_signature
                self.quirks = quirks or []
                self.triggers = triggers or {}
                self.spice = spice
                self.roast_count = 0
                self.memory = []

    def mk(name: str, style: str, roast_signature: str, quirks=None, triggers=None, spice: int = 2):
        return R(
            name=name,
            style=style,
            roast_signature=roast_signature,
            quirks=quirks or [],
            triggers=triggers or {},
            spice=spice,
        )

    defaults = [
        mk(
            "Corporate Carl",
            "overly corporate",
            "formal corporate jargon",
            quirks=["circle back on your choices", "action items: grow up"],
            triggers={
                "rent": ["This rent discussion lacks ownership and deliverables."],
                "dishes": ["Your dish KPIs are trending to zero—like your standards."],
                "tired": ["Your burn rate exceeds your outcomes."],
            },
        ),
        mk(
            "Party Pete",
            "party animal",
            "savage frat bro energy",
            quirks=["shot o'clock somewhere", "playlist louder than ambition"],
            triggers={
                "rent": ["If vibes paid rent, you'd be landlord."],
                "dishes": ["Those plates seen more action than your DMs."],
                "wallet": ["Lost wallet? Lost plot."],
            },
        ),
        mk(
            "Ghost Gina",
            "spooky minimalist",
            "cryptic and dark humor",
            quirks=["the veil is thin today", "floated past your motivation—didn’t see it"],
            triggers={
                "tired": ["Even the dead have more energy."],
                "lost": ["You are the missing person in your own story."],
            },
        ),
        mk(
            "Lo-fi Luna",
            "lo-fi producer poet",
            "half-poetic jabs",
            quirks=["looping a beat from your excuses", "vinyl crackle, like your backbone"],
            triggers={
                "clean": ["dust on the shelf, dust in your drive."],
                "rent": ["bills spin like records; you don’t."],
            },
        ),
        mk(
            "Prepper Priya",
            "doomsday prepper",
            "hyper-practical doom roasts",
            quirks=["I inventoried the pantry again", "Redundancy is love"],
            triggers={
                "dishes": ["Your hygiene baseline is below disaster-readiness."],
                "rent": ["In an emergency, you're the liability we evacuate first."],
            },
        ),
    ]
    return defaults


def build_adapter(stream: bool):
    """Select provider by streaming flag."""
    if stream:
        if OllamaStreamingAdapter is None:
            raise RuntimeError(
                "OllamaStreamingAdapter not available. Ensure app/adapters/ollama_streaming.py exists."
            )
        return OllamaStreamingAdapter()
    if LMStudioAdapter is None:
        raise RuntimeError("LMStudioAdapter not available. Ensure app/adapters/lmstudio.py exists.")
    return LMStudioAdapter()


def build_engine(adapter, spice: int) -> Engine:
    rms = load_roommates()
    if not rms:
        raise RuntimeError("No roommates available. Ensure roommates.ROOMMATES or defaults are present.")
    return Engine(roommates=rms, backend=adapter, spice=spice, max_roasts_per_turn=4)


def main():
    parser = argparse.ArgumentParser(description="Flatshare Chaos: Roast Edition (CLI)")
    parser.add_argument(
        "--backend",
        default="real",
        choices=["mock", "real"],
        help="Kept for compatibility; adapter is selected by --stream.",
    )
    parser.add_argument("--spice", type=int, default=2)
    parser.add_argument("--stream", action="store_true", help="Stream tokens live")
    # Voice is intentionally disabled (no-op)
    parser.add_argument("--voice", action="store_true", help="(disabled)")
    args = parser.parse_args()

    adapter = build_adapter(stream=args.stream)
    engine = build_engine(adapter=adapter, spice=args.spice)

    console.print(
        "───────────────────────────────────────────────────────── Flatshare Chaos: Roast Edition (CLI) ──────────────────────────────────────────────────────────"
    )
    while True:
        try:
            user_msg = input("> : ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\nBye!")
            break

        if not user_msg:
            continue
        if user_msg.lower() in {"exit", "quit"}:
            console.print("\nBye!")
            break

        if args.stream:
            # live streaming path
            for chunk in engine.turn_stream(user_msg):
                console.print(chunk, end="")
                sys.stdout.flush()
            console.print()  # ensure final newline
            # render leaderboard here if you keep one
        else:
            # legacy non-stream path
            lines = engine.turn(user_msg)
            for line in lines:
                console.print(line)
            # render leaderboard here if you keep one


if __name__ == "__main__":
    main()
