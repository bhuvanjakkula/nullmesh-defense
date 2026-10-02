from nullmesh.identity import Identity

def test_signature(tmp_path):
    i=Identity.load_or_create(str(tmp_path)); msg=b'nullmesh'
    assert Identity.verify(i.public_b64(), msg, i.sign(msg))
    assert not Identity.verify(i.public_b64(), b'tampered', i.sign(msg))
