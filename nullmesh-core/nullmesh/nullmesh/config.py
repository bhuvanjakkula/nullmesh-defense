from __future__ import annotations
from dataclasses import dataclass, field
import os

@dataclass(slots=True)
class Settings:
    node_name: str = field(default_factory=lambda: os.getenv("NULLMESH_NODE", "node-a"))
    host: str = field(default_factory=lambda: os.getenv("NULLMESH_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("NULLMESH_PORT", "8000")))
    data_dir: str = field(default_factory=lambda: os.getenv("NULLMESH_DATA", "./data"))
    peers: list[str] = field(default_factory=lambda: [p.strip().rstrip('/') for p in os.getenv("NULLMESH_PEERS", "").split(',') if p.strip()])
    forward_interval: float = field(default_factory=lambda: float(os.getenv("NULLMESH_FORWARD_INTERVAL", "2")))
    max_hops: int = field(default_factory=lambda: int(os.getenv("NULLMESH_MAX_HOPS", "16")))
