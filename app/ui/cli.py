import typer, re
from rich.console import Console
from rich.table import Table
from typing import Optional

from ..roommates import Roommate
from ..engine import Engine
from ..adapters.mock import MockAdapter
from ..adapters.lmstudio import LMStudioAdapter
from ..audio_manager import build_tts_engines

app = typer.Typer(add_completion=False)
console = Console()

def parse(line: str):
    m = re.match(r"^([^:]+):\s+(.*)$", line)
    return (m.group(1), m.group(2)) if m else (None, line)

@app.command()
def main(
    backend: str = typer.Option("mock", help="mock|lmstudio"),
    voice: bool = typer.Option(False, help="Speak roommate lines via macOS voices"),
    spice: int = typer.Option(2, min=0, max=3),
):
    rms = [
        Roommate("Corporate Carl","overly corporate","formal corporate jargon",
                 ["circle back on your choices","action items: grow up"],{"rent":["This rent discussion lacks ownership and deliverables."],"dishes":["Your dish KPIs are trending to zero—like your standards."],"tired":["Your burn rate exceeds your outcomes."]},spice=spice),
        Roommate("Party Pete","party animal","savage frat bro energy",
                 ["shot o'clock somewhere","playlist louder than ambition"],{"rent":["If vibes paid rent, you'd be landlord."],"dishes":["Those plates seen more action than your DMs."],"wallet":["Lost wallet? Lost plot."]},spice=spice),
        Roommate("Ghost Gina","spooky minimalist","cryptic and dark humor",
                 ["the veil is thin today","floated past your motivation—didn’t see it"],{"tired":["Even the dead have more energy."],"lost":["You are the missing person in your own story."]},spice=spice),
        Roommate("Lo-fi Luna","lo-fi producer poet","half-poetic jabs",
                 ["looping a beat from your excuses","vinyl crackle, like your backbone"],{"clean":["dust on the shelf, dust in your drive."],"rent":["bills spin like records; you don’t."]},spice=spice),
        Roommate("Prepper Priya","doomsday prepper","hyper-practical doom roasts",
                 ["I inventoried the pantry again","Redundancy is love"],{"dishes":["Your hygiene baseline is below disaster-readiness."],"rent":["In an emergency, you're the liability we evacuate first."]},spice=spice),
    ]
    adapter = MockAdapter() if backend=="mock" else LMStudioAdapter()
    engine = Engine(rms, backend=adapter, max_roasts_per_turn=4)

    tts_map = build_tts_engines([r.name for r in rms]) if voice else {}

    console.rule("[bold magenta]Flatshare Chaos: Roast Edition (CLI)")
    while True:
        try:
            user_msg = typer.prompt("> ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\nBye!"); break
        if not user_msg: 
            continue
        lines = engine.turn(user_msg)
        for line in lines:
            console.print(line)
            who, text = parse(line)
            if voice and who in tts_map:
                try:
                    tts_map[who].say(text); tts_map[who].runAndWait()
                except Exception as e:
                    console.print(f"[red]TTS error:[/red] {e}")
        # leaderboard
        table = Table(title="Roast Leaderboard")
        table.add_column("Rank"); table.add_column("Roommate"); table.add_column("Roasts", justify="right")
        for i,row in enumerate(engine.leaderboard(), start=1):
            name = row.split(" — ")[0].split(". ")[1]; count = row.split(" — ")[1].split()[0]
            table.add_row(str(i), name, count)
        console.print(table)

if __name__ == "__main__":
    app()
