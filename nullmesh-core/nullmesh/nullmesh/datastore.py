from __future__ import annotations
import sqlite3
from pathlib import Path
from .protocol import MeshObject

class Store:
    def __init__(self, directory: str):
        Path(directory).mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(Path(directory)/"nullmesh.db"), check_same_thread=False)
        self.db.execute("CREATE TABLE IF NOT EXISTS objects(id TEXT PRIMARY KEY, json TEXT NOT NULL, status TEXT NOT NULL)")
        self.db.commit()

    def put(self, obj: MeshObject, status="queued"):
        self.db.execute("INSERT OR REPLACE INTO objects VALUES(?,?,?)", (obj.object_id, obj.model_dump_json(), status)); self.db.commit()

    def has(self, oid: str) -> bool:
        return self.db.execute("SELECT 1 FROM objects WHERE id=?", (oid,)).fetchone() is not None

    def set_status(self, oid: str, status: str):
        self.db.execute("UPDATE objects SET status=? WHERE id=?", (status, oid)); self.db.commit()

    def list(self, status: str | None=None):
        rows = self.db.execute("SELECT json,status FROM objects" + (" WHERE status=?" if status else ""), ((status,) if status else ())).fetchall()
        return [(MeshObject.model_validate_json(j), s) for j,s in rows]
