from __future__ import annotations
from datetime import datetime, timezone
import hashlib, json, uuid
from pydantic import BaseModel, Field

class MeshObject(BaseModel):
    object_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    source: str
    destination: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: str | None = None
    priority: int = 5
    payload: str
    payload_hash: str = ""
    public_key: str
    signature: str = ""
    hops: list[str] = Field(default_factory=list)

    def canonical(self) -> bytes:
        d = self.model_dump(exclude={"signature"}, mode="json")
        return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()

    def compute_payload_hash(self) -> str:
        return hashlib.sha256(self.payload.encode()).hexdigest()
