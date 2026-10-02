from __future__ import annotations
from datetime import datetime, timezone
from .identity import Identity

class Forwarder:
    def __init__(self, node): self.node = node

    async def tick(self):
        await self.node.refresh_peers()
        for obj, status in self.node.store.list('queued'):
            if obj.destination == self.node.identity.node_id:
                self.node.store.set_status(obj.object_id, 'delivered'); continue
            if len(obj.hops) >= self.node.settings.max_hops: continue
            for peer in self.node.peers.values():
                if peer.node_id in obj.hops: continue
                try:
                    await self.node.transport.send(peer.url, obj)
                    self.node.store.set_status(obj.object_id, 'forwarded')
                    break
                except Exception:
                    peer.healthy = False
