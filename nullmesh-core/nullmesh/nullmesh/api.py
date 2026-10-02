from __future__ import annotations
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .protocol import MeshObject
from .identity import Identity

class SendRequest(BaseModel):
    destination: str
    payload: str
    priority: int = 5


def create_app(node):
    app = FastAPI(title="NullMesh", version="0.1.0")

    @app.on_event("startup")
    async def startup():
        app.state.worker = asyncio.create_task(node.run())

    @app.on_event("shutdown")
    async def shutdown():
        app.state.worker.cancel()

    @app.get('/v1/info')
    async def info():
        return {'node_id':node.identity.node_id,'name':node.settings.node_name,'public_key':node.identity.public_b64(),'peers':len(node.peers)}

    @app.get('/v1/objects')
    async def objects():
        return [{'object':o.model_dump(),'status':s} for o,s in node.store.list()]

    @app.post('/v1/send')
    async def send(req: SendRequest):
        obj = node.make_object(req.destination, req.payload, req.priority); node.store.put(obj)
        return {'object_id':obj.object_id,'status':'queued'}

    @app.post('/v1/receive')
    async def receive(obj: MeshObject):
        if obj.payload_hash != obj.compute_payload_hash(): raise HTTPException(400, 'payload hash mismatch')
        if not Identity.verify(obj.public_key, obj.canonical(), obj.signature): raise HTTPException(400, 'invalid signature')
        if node.store.has(obj.object_id): return {'status':'duplicate'}
        obj.hops.append(node.identity.node_id)
        node.store.put(obj, 'delivered' if obj.destination == node.identity.node_id else 'queued')
        return {'status':'accepted'}
    return app
