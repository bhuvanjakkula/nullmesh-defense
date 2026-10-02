from __future__ import annotations
import asyncio

async def periodic(interval, fn):
    while True:
        await fn(); await asyncio.sleep(interval)
