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
        self.conversation_history: List[str] = []  # Track conversation history
        self.max_history = 10  # Keep last 10 exchanges
    
    def _build_context(self) -> str:
        """Build conversation context from recent history."""
        if not self.conversation_history:
            return "CONVERSATION CONTEXT: This is the start of the conversation."
        
        # Get recent history (last few exchanges)
        recent_history = self.conversation_history[-6:]  # Last 6 messages
        context = "RECENT CONVERSATION:\n" + "\n".join(recent_history)
        return context
    
    def _add_to_history(self, message: str):
        """Add message to conversation history."""
        self.conversation_history.append(message)
        # Keep only recent history
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]

    # -----------------------
    # Existing non-stream path
    # -----------------------
    def primary(self, r: Roommate, user_msg: str) -> str:
        # Build context-aware system prompt
        context = self._build_context()
        sys = f"""You are {r.name}, style '{r.style}'. Be concise, witty, PG-13.

PERSONALITY DETAILS:
- Roast signature: {r.roast_signature}
- Quirks: {', '.join(r.quirks) if hasattr(r, 'quirks') and r.quirks else 'None'}

{context}

Respond in character, referencing the conversation history when relevant."""
        
        usr = f"User: {user_msg}"
        out = self.backend.generate(sys, usr, 0.7, 64).strip()
        return f"{r.name}: {out}"

    def roast(self, r: Roommate, target: str, user_msg: str) -> str:
        # Build context-aware roast prompt
        context = self._build_context()
        sys = f"""You are {r.name}. Single-line roast for {target} in style: {r.roast_signature}. Keep it tight.

PERSONALITY DETAILS:
- Style: {r.style}
- Quirks: {', '.join(r.quirks) if hasattr(r, 'quirks') and r.quirks else 'None'}

{context}

Make the roast reference the conversation history or the target's previous behavior when possible."""
        
        usr = f"User: {user_msg}"
        out = self.backend.generate(sys, usr, 0.8, 64).strip()
        return f"{r.name}: {out}"

    def turn(self, user_msg: str) -> List[str]:
        """Legacy non-streaming turn. Returns a list of fully-formed lines."""
        lines: List[str] = [f"You: {user_msg}"]
        
        # Add user message to history
        self._add_to_history(f"You: {user_msg}")

        primary = random.choice(self.roommates)
        primary_response = self.primary(primary, user_msg)
        lines.append(primary_response)
        
        # Add primary response to history
        self._add_to_history(primary_response)

        targets = ["you", primary.name]
        roasters = random.sample(self.roommates, k=min(len(self.roommates), self.max_roasts_per_turn))
        n = random.randint(2, min(self.max_roasts_per_turn, len(roasters)))
        for r in roasters[:n]:
            tgt = random.choice(targets)
            roast_response = self.roast(r, tgt, user_msg)
            lines.append(roast_response)
            
            # Add roast to history
            self._add_to_history(roast_response)

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
        # Build context-aware system prompt
        context = self._build_context()
        sys = f"""You are {r.name}, style '{r.style}'. Be concise, witty, PG-13.

PERSONALITY DETAILS:
- Roast signature: {r.roast_signature}
- Quirks: {', '.join(r.quirks) if hasattr(r, 'quirks') and r.quirks else 'None'}

{context}

Respond in character, referencing the conversation history when relevant."""
        
        usr = f"User: {user_msg}"
        # Prefix speaker once, then stream content
        yield f"{r.name}: "
        
        response_parts = []
        for chunk in self._gen_stream(sys, usr, 0.7, 64):
            response_parts.append(chunk)
            yield chunk
        
        # Add complete response to history
        complete_response = f"{r.name}: {''.join(response_parts)}"
        self._add_to_history(complete_response)

    def roast_stream(self, r: Roommate, target: str, user_msg: str) -> Iterator[str]:
        # Build context-aware roast prompt
        context = self._build_context()
        sys = f"""You are {r.name}. Single-line roast for {target} in style: {r.roast_signature}. Keep it tight.

PERSONALITY DETAILS:
- Style: {r.style}
- Quirks: {', '.join(r.quirks) if hasattr(r, 'quirks') and r.quirks else 'None'}

{context}

Make the roast reference the conversation history or the target's previous behavior when possible."""
        
        usr = f"User: {user_msg}"
        yield f"{r.name}: "
        
        response_parts = []
        for chunk in self._gen_stream(sys, usr, 0.8, 64):
            response_parts.append(chunk)
            yield chunk
        
        # Add complete roast to history
        complete_roast = f"{r.name}: {''.join(response_parts)}"
        self._add_to_history(complete_roast)

    def turn_stream(self, user_msg: str) -> Iterator[str]:
        """
        Stream an entire turn serially (clean in terminal):
        - print the user's line
        - stream primary roommate
        - stream a few roasters
        """
        yield f"You: {user_msg}\n"
        
        # Add user message to history
        self._add_to_history(f"You: {user_msg}")

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
