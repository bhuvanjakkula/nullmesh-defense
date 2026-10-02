from __future__ import annotations
import argparse, asyncio
import uvicorn
from .config import Settings
from .identity import Identity
from .datastore import Store
from .transport import HTTPTransport
from .discovery import discover
from .forwarding import Forwarder
from .protocol import MeshObject
from .api import create_app

class NullNode:
    def __init__(self, settings: Settings):
        self.settings=settings; self.identity=Identity.load_or_create(settings.data_dir)
        self.store=Store(settings.data_dir); self.transport=HTTPTransport(); self.peers={}
        self.forwarder=Forwarder(self)
    async def refresh_peers(self):
        for p in await discover(self.settings.peers, self.transport): self.peers[p.node_id]=p
    def make_object(self, destination, payload, priority=5):
        o=MeshObject(source=self.identity.node_id,destination=destination,payload=payload,priority=priority,public_key=self.identity.public_b64(),hops=[self.identity.node_id])
        o.payload_hash=o.compute_payload_hash(); o.signature=self.identity.sign(o.canonical()); return o
    async def run(self):
        while True:
            await self.forwarder.tick(); await asyncio.sleep(self.settings.forward_interval)

def cli():
    p=argparse.ArgumentParser(description='NullMesh defensive DTN prototype'); p.add_argument('command', choices=['serve','id']); p.add_argument('--port',type=int)
    a=p.parse_args(); s=Settings();
    if a.port: s.port=a.port
    n=NullNode(s)
    if a.command=='id': print(n.identity.node_id); return
    uvicorn.run(create_app(n), host=s.host, port=s.port)

if __name__ == '__main__': cli()
