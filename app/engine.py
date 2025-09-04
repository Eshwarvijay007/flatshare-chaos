# app/engine.py
# Engine with both non-stream and stream paths.
# Assumptions (from your repo/traceback):
# - You have a Roommate type/class with attributes:
#   name, style, roast_signature, spice, roast_count, memory, triggers (dict)
# - You construct Engine(roommates=[...], backend=adapter, spice=int, max_roasts_per_turn=int, ...)
# - backend (or adapter) has .generate(system, user, temperature, max_tokens) -> str
#   Optionally it may also have .generate_stream(...)-> Iterator[str] (for streaming)

from __future__ import annotations
import random
from typing import Iterator, List, Any

try:
    # If you have a typed Roommate definition somewhere
    from roommates import Roommate  # type: ignore
except Exception:  # fallback typing for linters
    class Roommate:  # type: ignore
        name: str
        style: str
        roast_signature: str
        spice: int
        roast_count: int
        memory: list
        triggers: dict

class Engine:
    def __init__(
        self,
        roommates: List[Roommate],
        backend: Any,
        spice: int = 2,
        max_roasts_per_turn: int = 4,
    ):
        self.roommates = roommates
        self.backend = backend  # may also be known as "adapter" elsewhere
        self.spice = spice
        self.max_roasts_per_turn = max_roasts_per_turn

    # -----------------------
    # Existing non-stream path
    # -----------------------
    def primary(self, r: Roommate, user_msg: str) -> str:
        sys = f"You are {r.name}, style '{r.style}'. Be concise, witty, PG-13."
        usr = f"User: {user_msg}"
        out = self.backend.generate(sys, usr, 0.7, 64).strip()
        return f"{r.name}: {out}"

    def roast(self, r: Roommate, target: str, user_msg: str) -> str:
        sys = f"You are {r.name}. Single-line roast for {target} in style: {r.roast_signature}. Keep it tight."
        usr = f"User: {user_msg}"
        out = self.backend.generate(sys, usr, 0.8, 64).strip()
        return f"{r.name}: {out}"

    def turn(self, user_msg: str) -> List[str]:
        """Legacy non-streaming turn. Returns a list of fully-formed lines."""
        lines: List[str] = [f"You: {user_msg}"]

        primary = random.choice(self.roommates)
        lines.append(self.primary(primary, user_msg))

        targets = ["you", primary.name]
        roasters = random.sample(self.roommates, k=min(len(self.roommates), self.max_roasts_per_turn))
        n = random.randint(2, min(self.max_roasts_per_turn, len(roasters)))
        for r in roasters[:n]:
            tgt = random.choice(targets)
            lines.append(self.roast(r, tgt, user_msg))

        return lines

    # -----------------------
    # Streaming path (new)
    # -----------------------
    def _provider(self) -> Any:
        """Return the generation provider (backend/adapter)."""
        # If you later mount an "adapter", prefer that; else use "backend"
        return getattr(self, "adapter", None) or self.backend

    def _gen_stream(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
    ) -> Iterator[str]:
        """
        Unified stream generator:
        - If provider has .generate_stream(...), yield chunks as they arrive.
        - Otherwise, fall back to one-shot .generate(...) and yield once.
        """
        provider = self._provider()
        if hasattr(provider, "generate_stream"):
            for chunk in provider.generate_stream(system_prompt, user_prompt, temperature, max_tokens):
                if chunk:
                    yield chunk
        else:
            text = provider.generate(system_prompt, user_prompt, temperature, max_tokens)
            if text:
                yield text

    def primary_stream(self, r: Roommate, user_msg: str) -> Iterator[str]:
        sys = f"You are {r.name}, style '{r.style}'. Be concise, witty, PG-13."
        usr = f"User: {user_msg}"
        # Prefix speaker once, then stream content
        yield f"{r.name}: "
        for chunk in self._gen_stream(sys, usr, 0.7, 64):
            yield chunk

    def roast_stream(self, r: Roommate, target: str, user_msg: str) -> Iterator[str]:
        sys = f"You are {r.name}. Single-line roast for {target} in style: {r.roast_signature}. Keep it tight."
        usr = f"User: {user_msg}"
        yield f"{r.name}: "
        for chunk in self._gen_stream(sys, usr, 0.8, 64):
            yield chunk

    def turn_stream(self, user_msg: str) -> Iterator[str]:
        """
        Stream an entire turn serially (clean in terminal):
        - print the user's line
        - stream primary roommate
        - stream a few roasters
        """
        yield f"You: {user_msg}\n"

        primary = random.choice(self.roommates)
        for chunk in self.primary_stream(primary, user_msg):
            yield chunk
        yield "\n"

        targets = ["you", primary.name]
        roasters = random.sample(self.roommates, k=min(len(self.roommates), self.max_roasts_per_turn))
        n = random.randint(2, min(self.max_roasts_per_turn, len(roasters)))
        for r in roasters[:n]:
            tgt = random.choice(targets)
            for chunk in self.roast_stream(r, tgt, user_msg):
                yield chunk
            yield "\n"
