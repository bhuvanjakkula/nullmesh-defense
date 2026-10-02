from nullmesh.main import NullNode
from nullmesh.config import Settings
from nullmesh.identity import Identity

def test_object_signature(tmp_path):
    n=NullNode(Settings(data_dir=str(tmp_path)))
    o=n.make_object('destination','hello')
    assert o.payload_hash == o.compute_payload_hash()
    assert Identity.verify(o.public_key,o.canonical(),o.signature)
