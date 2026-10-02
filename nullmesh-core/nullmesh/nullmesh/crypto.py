"""Small cryptographic helpers. NullMesh intentionally relies on established primitives."""
from __future__ import annotations
import hashlib

def content_id(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
