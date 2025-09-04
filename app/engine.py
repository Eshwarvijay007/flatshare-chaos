import random
from typing import List
from .roommates import Roommate
from .safety.filters import sanitize_roast

class Engine:
    def __init__(self, roommates: List[Roommate], backend, max_roasts_per_turn: int = 4, seed: int = 42):
        self.roommates = roommates
        self.backend = backend
        self.max_roasts_per_turn = max_roasts_per_turn
        random.seed(seed)
    def primary(self, r: Roommate, user_msg: str) -> str:
        sys = f"You are {r.name}, style '{r.style}'. Be concise, witty, PG-13."
        usr = f"User: {user_msg}"
        out = self.backend.generate(sys, usr, 0.7, 64).strip()
        return f"{r.name}: {out}"
    def roast(self, r: Roommate, target: str, user_msg: str) -> str:
        sys = f"You are {r.name}. Single-line roast for {target} in style: {r.roast_signature}. PG-13 only."
        base = None
        for k, lines in r.triggers.items():
            if k in user_msg.lower():
                base = random.choice(lines); break
        usr = f"User: {user_msg}. If base fits, refine: '{base or ''}'. One line."
        out = self.backend.generate(sys, usr, 0.9, 48).strip()
        out = sanitize_roast(out)
        r.roast_count += 1
        return f"{r.name}: {out}"
    def turn(self, user_msg: str) -> List[str]:
        t = [f"You: {user_msg}"]
        primary = random.choice(self.roommates)
        t.append(self.primary(primary, user_msg))
        targets = ["you", primary.name]
        roasters = random.sample(self.roommates, k=min(len(self.roommates), self.max_roasts_per_turn))
        n = random.randint(2, min(self.max_roasts_per_turn, len(roasters)))
        for i in range(n):
            r = roasters[i]
            t.append(self.roast(r, random.choice(targets), user_msg))
        if random.random() < 0.4 and len(self.roommates)>=2:
            a,b = random.sample(self.roommates,2)
            t.append(self.roast(a, b.name, user_msg))
        return t
    def leaderboard(self) -> List[str]:
        sorted_rm = sorted(self.roommates, key=lambda r: r.roast_count, reverse=True)
        return [f"{i+1}. {rm.name} — {rm.roast_count} roasts" for i, rm in enumerate(sorted_rm)]
