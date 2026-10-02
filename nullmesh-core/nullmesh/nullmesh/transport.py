from __future__ import annotations
import httpx
from .protocol import MeshObject

class HTTPTransport:
    def __init__(self, timeout=2.0): self.timeout = timeout
    async def info(self, url: str):
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            r = await c.get(url.rstrip('/') + '/v1/info'); r.raise_for_status(); return r.json()
    async def send(self, url: str, obj: MeshObject):
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            r = await c.post(url.rstrip('/') + '/v1/receive', json=obj.model_dump()); r.raise_for_status(); return r.json()
