from __future__ import annotations
from collections import deque

class RoutingTable:
    def __init__(self):
        self.graph: dict[str, set[str]] = {}

    def add_link(self, a: str, b: str):
        self.graph.setdefault(a, set()).add(b); self.graph.setdefault(b, set()).add(a)

    def remove_link(self, a: str, b: str):
        self.graph.get(a, set()).discard(b); self.graph.get(b, set()).discard(a)

    def next_hop(self, source: str, destination: str) -> str | None:
        if source == destination: return destination
        q = deque([(source, None)]); seen = {source}
        while q:
            node, first = q.popleft()
            for nxt in sorted(self.graph.get(node, ())):
                if nxt in seen: continue
                nf = nxt if first is None else first
                if nxt == destination: return nf
                seen.add(nxt); q.append((nxt, nf))
        return None
