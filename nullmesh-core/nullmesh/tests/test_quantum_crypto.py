import pytest
from nullmesh.quantum_crypto import MLKEM768, MLDSA65, QKDSimulator, QuantumCryptoEnclave

def test_mlkem_key_encapsulation():
    pub, priv = MLKEM768.generate_keypair()
    shared_alice, ciphertext = MLKEM768.encapsulate(pub)
    shared_bob = MLKEM768.decapsulate(priv, ciphertext)
    assert len(shared_alice) == 32
    assert len(shared_bob) == 32
    assert len(ciphertext) == 64

def test_mldsa_signature():
    pub, priv = MLDSA65.generate_keypair()
    msg = b"CRITICAL_TACTICAL_COMMAND_ROUTING"
    sig = MLDSA65.sign(priv, msg)
    assert MLDSA65.verify(pub, msg, sig) is True
    assert MLDSA65.verify(pub, msg, b"corrupted_short_signature") is False

def test_qkd_secure_exchange():
    qkd = QKDSimulator(key_length_bits=128)
    res = qkd.exchange(eavesdropping=False)
    assert res["status"] == "SECURE_KEY_GENERATED"
    assert res["qber"] < 11.0
    assert res["qkd_session_key"] is not None

def test_qkd_eavesdropping_detection():
    qkd = QKDSimulator(key_length_bits=128)
    res = qkd.exchange(eavesdropping=True)
    assert res["eavesdropping_detected"] is True
    assert res["qber"] > 15.0
    assert res["status"] == "ABORT_EAVESDROPPER_DETECTED"
    assert res["qkd_session_key"] is None

def test_quantum_crypto_enclave_e2e():
    node_a = QuantumCryptoEnclave()
    node_b = QuantumCryptoEnclave()

    plaintext = "CONFIDENTIAL: Land-Sea-Space Tactical Defense Packet"
    encrypted_envelope = node_a.encrypt_payload(plaintext, node_b.kem_pub)

    assert encrypted_envelope["cipher"] == "AES-256-GCM-PQC-HYBRID"
    assert encrypted_envelope["ciphertext"] != plaintext

    decrypted = node_b.decrypt_payload(encrypted_envelope)
    assert decrypted == plaintext
