from __future__ import annotations
from .peer import Peer

async def discover(urls, transport):
    found = []
    for url in urls:
        try:
            i = await transport.info(url)
            found.append(Peer(i['node_id'], i['name'], url, i['public_key']))
        except Exception:
            continue
    return found
