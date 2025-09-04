"""
Enhanced CLI with unique personality-driven interactions.
"""

import argparse
import sys
import time
from typing import Tuple, List, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Import our new personality system
from app.personality_profiles import create_flatshare_chaos_roommates
from app.personality_engine import PersonalityEngine

# Adapters
try:
    from app.adapters.ollama_streaming import OllamaStreamingAdapter
except Exception:
    OllamaStreamingAdapter = None

try:
    from app.adapters.lmstudio import LMStudioAdapter
except Exception:
    LMStudioAdapter = None

console = Console()

# Personality-specific colors for better visual distinction
PERSONALITY_COLORS = {
    "CodeMaster": "bright_blue",
    "SavageBurn": "bright_red", 
    "UncleJi": "yellow",
    "ChefCritic": "green",
    "BeatDrop": "magenta",
    "ChaosKing": "bright_black",
    "QuietStorm": "cyan",
    "PennyPincher": "bright_yellow",
    "DeepThought": "bright_magenta",
    "_you": "bold white",
    "_default": "white"
}

PAUSE_S = 0.03


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


def display_roommate_intro():
    """Display an introduction to all the unique roommates."""
    console.print("\n[bold bright_cyan]🏠 Welcome to the Flatshare Chaos! 🏠[/bold bright_cyan]")
    console.print("[dim]Meet your chaotic roommates...[/dim]\n")
    
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
        color = PERSONALITY_COLORS.get(name, "white")
        table.add_row(
            f"[{color}]{name}[/{color}]",
            desc,
            style,
            quirk
        )
    
    console.print(table)
    console.print("\n[dim]Each roommate has unique triggers, speech patterns, and interaction dynamics![/dim]")
    console.print("[dim]Type 'relationships' to see how they get along with each other.[/dim]")
    console.print("[dim]Type 'help' for more commands.[/dim]\n")


def display_relationships(engine: PersonalityEngine):
    """Display current relationship status between roommates."""
    relationships = engine.get_relationship_status()
    
    console.print("\n[bold bright_cyan]🤝 Roommate Relationships 🤝[/bold bright_cyan]")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Roommate", style="bold", width=12)
    
    # Add columns for each roommate
    roommate_names = list(relationships.keys())
    for name in roommate_names:
        color = PERSONALITY_COLORS.get(name, "white")
        table.add_column(f"[{color}]{name[:8]}[/{color}]", width=8, justify="center")
    
    # Add rows
    for roommate_name in roommate_names:
        color = PERSONALITY_COLORS.get(roommate_name, "white")
        row = [f"[{color}]{roommate_name}[/{color}]"]
        
        for other_name in roommate_names:
            if roommate_name == other_name:
                row.append("[dim]--[/dim]")
            else:
                score = relationships[roommate_name].get(other_name, 50)
                if score >= 70:
                    row.append(f"[green]{score}[/green]")
                elif score >= 40:
                    row.append(f"[yellow]{score}[/yellow]")
                else:
                    row.append(f"[red]{score}[/red]")
        
        table.add_row(*row)
    
    console.print(table)
    console.print("\n[dim]Scores: [green]70+[/green] = Good friends, [yellow]40-69[/yellow] = Neutral, [red]<40[/red] = Tension[/dim]\n")


def display_help():
    """Display available commands."""
    help_panel = Panel(
        """[bold]Available Commands:[/bold]

• [cyan]relationships[/cyan] - View roommate relationship status
• [cyan]personalities[/cyan] - Show roommate personality profiles  
• [cyan]stats[/cyan] - Display interaction statistics
• [cyan]help[/cyan] - Show this help message
• [cyan]exit/quit[/cyan] - Leave the flatshare

[bold]How it works:[/bold]
Each roommate has a unique personality with specific triggers, speech patterns, and roasting styles. 
They interact differently based on the topic, their relationships, and their individual quirks.
The more you chat, the more their relationships evolve!""",
        title="[bold bright_cyan]Flatshare Chaos Help[/bold bright_cyan]",
        border_style="cyan"
    )
    console.print(help_panel)


def display_stats(engine: PersonalityEngine):
    """Display interaction statistics."""
    console.print("\n[bold bright_cyan]📊 Interaction Statistics 📊[/bold bright_cyan]")
    
    total_interactions = len(engine.interaction_history)
    if total_interactions == 0:
        console.print("[dim]No interactions yet! Start chatting to see statistics.[/dim]\n")
        return
    
    # Count interactions per roommate
    roommate_counts = {}
    user_messages = 0
    
    for entry in engine.interaction_history:
        if entry.speaker == "user":
            user_messages += 1
        else:
            roommate_counts[entry.speaker] = roommate_counts.get(entry.speaker, 0) + 1
    
    # Display stats
    stats_table = Table(show_header=True, header_style="bold magenta")
    stats_table.add_column("Roommate", style="bold", width=12)
    stats_table.add_column("Messages", width=10, justify="center")
    stats_table.add_column("Activity Level", width=15)
    
    for roommate in engine.roommates:
        count = roommate_counts.get(roommate.name, 0)
        color = PERSONALITY_COLORS.get(roommate.name, "white")
        
        if count == 0:
            activity = "[dim]Silent[/dim]"
        elif count < 3:
            activity = "[yellow]Quiet[/yellow]"
        elif count < 6:
            activity = "[green]Active[/green]"
        else:
            activity = "[bright_green]Very Active[/bright_green]"
        
        stats_table.add_row(
            f"[{color}]{roommate.name}[/{color}]",
            str(count),
            activity
        )
    
    console.print(stats_table)
    console.print(f"\n[dim]Total messages: {total_interactions} | Your messages: {user_messages}[/dim]\n")


def main():
    parser = argparse.ArgumentParser(description="Flatshare Chaos: Personality Edition")
    parser.add_argument("--stream", action="store_true", help="Stream responses live")
    parser.add_argument("--spice", type=int, default=3, help="Roast intensity (1-5)")
    args = parser.parse_args()

    # Build adapter and engine
    adapter = build_adapter(stream=args.stream)
    roommates = create_flatshare_chaos_roommates()
    engine = PersonalityEngine(roommates, adapter)

    # Display intro
    display_roommate_intro()

    console.print("───────────────────────────────────────────────────────── [bold bright_cyan]Flatshare Chaos: Personality Edition[/bold bright_cyan] ─────────────────────────────────────────────────────────")
    
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
        elif user_msg.lower() == "relationships":
            display_relationships(engine)
            continue
        elif user_msg.lower() == "personalities":
            display_roommate_intro()
            continue
        elif user_msg.lower() == "stats":
            display_stats(engine)
            continue
        elif user_msg.lower() == "help":
            display_help()
            continue

        # Generate personality-driven responses
        if args.stream:
            # Streaming with personality colors
            current_speaker: str | None = None
            current_style: str = PERSONALITY_COLORS["_default"]

            for chunk in engine.personality_turn_stream(user_msg):
                # Newline indicates speaker finished
                if chunk == "\n":
                    console.print()
                    current_speaker = None
                    current_style = PERSONALITY_COLORS["_default"]
                    time.sleep(PAUSE_S)
                    continue

                # Detect speaker prefix
                if chunk.endswith(": ") and ":" in chunk:
                    speaker = chunk.split(":", 1)[0].strip()
                    current_speaker = speaker
                    if speaker == "You":
                        current_style = PERSONALITY_COLORS.get("_you", "bold white")
                    else:
                        current_style = PERSONALITY_COLORS.get(speaker, PERSONALITY_COLORS["_default"])
                    console.print(chunk, style=current_style, end="")
                else:
                    # Regular content chunk
                    console.print(chunk, style=current_style, end="")

                sys.stdout.flush()
                time.sleep(PAUSE_S)

            console.print()

        else:
            # Non-streaming mode
            responses = engine.personality_turn(user_msg)
            for response in responses:
                # Parse speaker and message
                if ":" in response:
                    speaker, message = response.split(":", 1)
                    speaker = speaker.strip()
                    message = message.strip()
                    
                    if speaker == "You":
                        style = PERSONALITY_COLORS.get("_you", "bold white")
                    else:
                        style = PERSONALITY_COLORS.get(speaker, PERSONALITY_COLORS["_default"])
                    
                    console.print(f"{speaker}: {message}", style=style)
                else:
                    console.print(response)


if __name__ == "__main__":
    main()