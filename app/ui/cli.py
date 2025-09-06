# app/ui/cli.py
from __future__ import annotations

import argparse
import sys
import time
from typing import Tuple, List, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Engine
from app.engine import Engine
from app.audio_manager import AudioManager

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

# ──────────────────────────────────────────────────────────────────────────────
# Config: colors & timing
# ──────────────────────────────────────────────────────────────────────────────

# Rich styles per roommate (tweak as you like)
CHARACTER_COLORS = {
    # Original roommates
    
    # New personality roommates
    "CodeMaster": "bright_blue",
    "SavageBurn": "bright_red", 
    "UncleJi": "yellow",
    "ChefCritic": "green",
    "BeatDrop": "magenta",
    "ChaosKing": "bright_black",
    "QuietStorm": "cyan",
    "PennyPincher": "bright_yellow",
    "DeepThought": "bright_magenta",
    # fallback color used if roommate not in this map
    "_default": "white",
    # color for the "You: ..." prefix
    "_you": "bold white",
}

# Pause per streamed chunk (seconds). Increase to slow down typing effect.
PAUSE_S = 0.03


def display_roommate_intro():
    """Display an introduction to all the unique roommates."""
    console.print("\n[bold bright_cyan]🏠 Welcome to the Flatshare Chaos! 🏠[/bold bright_cyan]")
    console.print("[dim]Meet your chaotic roommates...[/dim]\n")
    
    try:
        from app.personality_profiles import create_flatshare_chaos_roommates
        roommates = create_flatshare_chaos_roommates()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Roommate", style="bold", width=12)
        table.add_column("Personality", width=20)
        table.add_column("Signature Style", width=30)
        table.add_column("Key Quirk", width=25)
        
        personality_descriptions = {
            "CodeMaster": ("Tech Nerd", "Technical superiority burns", "Uses programming terms daily"),
            "SavageBurn": ("Professional Roaster", "Devastating one-liners", "Never misses a roast opportunity"),
            "UncleJi": ("Indian Uncle", "Disappointed uncle energy", "Compares everything to India"),
            "ChefCritic": ("Food Snob", "Culinary superiority complex", "Judges everyone's cooking"),
            "BeatDrop": ("DJ Party Guy", "Music-based burns", "Life revolves around beats"),
            "ChaosKing": ("Messy Rebel", "Chaotic deflection", "Organized chaos is still organized"),
            "QuietStorm": ("Shy Observer", "Innocent savage burns", "Soft-spoken but deadly"),
            "PennyPincher": ("Extreme Cheapskate", "Money-shaming guilt trips", "Calculates cost of everything"),
            "DeepThought": ("Overthinking Philosopher", "Existential confusion", "Turns everything into philosophy")
        }
        
        for roommate in roommates:
            name = roommate.name
            desc, style, quirk = personality_descriptions.get(name, ("Unknown", "Generic", "Mysterious"))
            color = CHARACTER_COLORS.get(name, "white")
            table.add_row(
                f"[{color}]{name}[/{color}]",
                desc,
                style,
                quirk
            )
        
        console.print(table)
        console.print("\n[dim]Each roommate has unique triggers, speech patterns, and interaction dynamics![/dim]")
        console.print("[dim]Type 'help' for available commands.[/dim]\n")
        
    except Exception:
        # Fallback for original roommates
        console.print("[dim]Using original roommate personalities...[/dim]\n")


def display_help():
    """Display available commands."""
    help_panel = Panel(
        """[bold]Available Commands:[/bold]

• [cyan]help[/cyan] - Show this help message
• [cyan]personalities[/cyan] - Show roommate personality profiles  
• [cyan]exit/quit[/cyan] - Leave the flatshare

[bold]How it works:[/bold]
Each roommate has a unique personality with specific triggers, speech patterns, and roasting styles. 
They respond differently based on the topic and their individual quirks.
Just chat naturally and watch the chaos unfold!""",
        title="[bold bright_cyan]Flatshare Chaos Help[/bold bright_cyan]",
        border_style="cyan"
    )
    console.print(help_panel)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

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
    try:
        from app import roommates as rm  # type: ignore
        return rm
    except Exception:
        pass
    try:
        import roommates as rm  # type: ignore
        return rm
    except Exception:
        return None


def load_roommates() -> List[object]:
    """
    Load roommates robustly:
      - Try to use new personality system first
      - Fall back to original roommates if needed
    """
    try:
        # Try to use the new personality system
        from app.personality_profiles import create_flatshare_chaos_roommates
        roommates = create_flatshare_chaos_roommates()
        if roommates:
            return roommates
    except Exception:
        pass
    
    rm = _load_roommates_module()

    # 1) Provided list
    if rm is not None and hasattr(rm, "ROOMMATES"):
        try:
            lst = getattr(rm, "ROOMMATES")
            if isinstance(lst, list) and len(lst) > 0:
                return lst
        except Exception:
            pass

    # 2) Factory functions
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

    # 3) Inline defaults
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
    
    # Always use the original engine for now - it works better
    return Engine(roommates=rms, backend=adapter, spice=spice, max_roasts_per_turn=4)


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

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
    parser.add_argument("--voice", action="store_true", help="Enable text-to-speech voice output.")
    # Optional: override pause/color via flags later if you want
    args = parser.parse_args()

    adapter = build_adapter(stream=args.stream)
    engine = build_engine(adapter=adapter, spice=args.spice)
    
    audio_manager = None
    if args.voice:
        audio_manager = AudioManager()

    # Display intro
    display_roommate_intro()

    console.print(
        "───────────────────────────────────────────────────────── [bold bright_cyan]Flatshare Chaos: Roast Edition (CLI)[/bold bright_cyan] ──────────────────────────────────────────────────────────"
    )
    while True:
        try:
            user_msg = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[bright_cyan]Thanks for visiting the chaos! 👋[/bright_cyan]")
            break

        if not user_msg:
            continue
            
        # Handle special commands
        if user_msg.lower() in {"exit", "quit"}:
            console.print("\n[bright_cyan]Thanks for visiting the chaos! 👋[/bright_cyan]")
            break
        elif user_msg.lower() == "personalities":
            display_roommate_intro()
            continue
        elif user_msg.lower() == "help":
            display_help()
            continue

        if args.stream:
            # Streaming with per-roommate colors + pause per chunk
            current_speaker: str | None = None
            current_style: str = CHARACTER_COLORS["_default"]
            full_line_buffer = ""


            for chunk in engine.turn_stream(user_msg):
                # Newline indicates speaker finished
                if chunk == "\n":
                    if audio_manager and current_speaker and full_line_buffer:
                        # Only use TTS for roommates (not "You"), and clean the text
                        if current_speaker != "You" and current_speaker in audio_manager.voices:
                            # Remove any speaker prefix that might be in the buffer
                            clean_text = full_line_buffer.strip()
                            if clean_text:
                                audio_manager.say(clean_text, current_speaker)

                    console.print()  # newline
                    current_speaker = None
                    current_style = CHARACTER_COLORS["_default"]
                    full_line_buffer = ""
                    time.sleep(PAUSE_S)
                    continue

                # Detect a speaker prefix (the engine yields "<Name>: " once before content)
                if chunk.endswith(": ") and ":" in chunk:
                    speaker = chunk.split(":", 1)[0].strip()
                    current_speaker = speaker
                    if speaker == "You":
                        current_style = CHARACTER_COLORS.get("_you", "bold white")
                    else:
                        current_style = CHARACTER_COLORS.get(speaker, CHARACTER_COLORS["_default"])
                    console.print(chunk, style=current_style, end="")
                else:
                    # Regular content chunk; use the last known speaker style
                    full_line_buffer += chunk
                    console.print(chunk, style=current_style, end="")

                sys.stdout.flush()
                time.sleep(PAUSE_S)

            # Ensure final newline after turn
            console.print()

        else:
            # Legacy non-stream path (no typewriter, no per-chunk pause)
            lines = engine.turn(user_msg)
            for line in lines:
                who, text = parse_spoken_line(line)
                style = CHARACTER_COLORS.get(who or "", CHARACTER_COLORS["_default"])
                if who == "You":
                    style = CHARACTER_COLORS.get("_you", "bold white")
                
                console.print(line, style=style)

                if audio_manager and who and text:
                    # Only use TTS for roommates (not "You"), and ensure they have voices
                    if who != "You" and who in audio_manager.voices:
                        audio_manager.say(text, who)



if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
