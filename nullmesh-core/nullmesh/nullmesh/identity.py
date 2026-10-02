from __future__ import annotations
import base64, hashlib, json
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

class Identity:
    def __init__(self, private_key: Ed25519PrivateKey):
        self.private_key = private_key
        self.public_key = private_key.public_key()
        raw = self.public_key.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        self.node_id = hashlib.sha256(raw).hexdigest()[:32]

    @classmethod
    def load_or_create(cls, directory: str) -> "Identity":
        path = Path(directory); path.mkdir(parents=True, exist_ok=True)
        keyfile = path / "identity.key"
        if keyfile.exists():
            key = Ed25519PrivateKey.from_private_bytes(base64.b64decode(keyfile.read_text().strip()))
        else:
            key = Ed25519PrivateKey.generate()
            raw = key.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption())
            keyfile.write_text(base64.b64encode(raw).decode())
        return cls(key)

    def public_b64(self) -> str:
        raw = self.public_key.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        return base64.b64encode(raw).decode()

    def sign(self, data: bytes) -> str:
        return base64.b64encode(self.private_key.sign(data)).decode()

    @staticmethod
    def verify(public_b64: str, data: bytes, signature_b64: str) -> bool:
        try:
            Ed25519PublicKey.from_public_bytes(base64.b64decode(public_b64)).verify(base64.b64decode(signature_b64), data)
            return True
        except Exception:
            return False
