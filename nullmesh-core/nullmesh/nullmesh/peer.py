from __future__ import annotations
from dataclasses import dataclass
from time import time

@dataclass
class Peer:
    node_id: str
    name: str
    url: str
    public_key: str
    last_seen: float = 0.0
    healthy: bool = True

    def touch(self):
        self.last_seen = time(); self.healthy = True
