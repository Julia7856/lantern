"""
Lantern - end-to-end session demo v3 (full Double Ratchet).
Демо сквозной сессии v3 (полный Double Ratchet).

did:key identity + hybrid KEM (X25519 + ML-KEM-768) + AES-256-GCM +
Ed25519 signature + Double Ratchet (DH + symmetric):
per-message keys + self-healing after compromise.
did:key идентичность + гибридный KEM (X25519 + ML-KEM-768) + AES-256-GCM +
подпись Ed25519 + Double Ratchet (DH + симметричный):
ключ на каждое сообщение + самолечение после компрометации.

Requires: pip install kyber-py cryptography
"""

import hashlib
import os

from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from kyber_py.ml_kem import ML_KEM_768

from crypto.session_ratchet import DoubleRatchet
from identity.did_key import create_did, sign_message, verify_message


def hybrid_session_key() -> bytes:
    """Hybrid shared key: X25519 + ML-KEM-768 -> SHA-256 / гибридный общий ключ."""
    xa = X25519PrivateKey.generate()
    xb = X25519PrivateKey.generate()
    x_shared = xa.exchange(xb.public_key())

    ek, dk = ML_KEM_768.keygen()
    k_bob, ct = ML_KEM_768.encaps(ek)
    k_alice = ML_KEM_768.decaps(dk, ct)
    assert k_alice == k_bob

    return hashlib.sha256(x_shared + k_alice).digest()


def encrypt(text: bytes, mk: bytes, sender: dict) -> dict:
    """Encrypt + sign / зашифровать + подписать."""
    nonce = os.urandom(12)
    ct = AESGCM(mk).encrypt(nonce, text, None)
    sig = sign_message(sender["private_key"], ct)
    return {"nonce": nonce, "ct": ct, "sig": sig}


def decrypt(env: dict, mk: bytes, sender_pub) -> bytes:
    """Verify + decrypt / проверить подпись + расшифровать."""
    assert verify_message(sender_pub, env["sig"], env["ct"])
    return AESGCM(mk).decrypt(env["nonce"], env["ct"], None)


if __name__ == "__main__":
    print("🏮 Lantern session demo v3 / демо сессии Lantern v3")
    print("=" * 56)

    # 1. Identities / идентичности
    alice_id = create_did()
    bob_id = create_did()
    print("👤 Alice & Bob identities created / идентичности созданы")

    # 2. Post-quantum root / постквантовый корень
    root = hybrid_session_key()
    print(f"🔐 Hybrid root (X25519 + ML-KEM) / гибридный корень: {len(root)} bytes")

    # 3. Double Ratchet on top of the hybrid root / Double Ratchet поверх корня
    alice = DoubleRatchet("Alice")
    bob = DoubleRatchet("Bob")
    alice.root = root
    bob.root = root
    alice.init_as_sender(bob.public())
    bob.init_as_receiver(alice.public())

    a_pub = alice_id["private_key"].public_key()
    b_pub = bob_id["private_key"].public_key()

    # msg 1: Alice -> Bob / сообщение 1
    mk_s = alice.send_key()
    env = encrypt("Hello Bob, this is Alice! / Привет, Боб, это Алиса!".encode("utf-8"), mk_s, alice_id)
    mk_r = bob.recv_key()
    plain = decrypt(env, mk_r, a_pub)
    print(f"📨 1. Alice -> Bob: {plain.decode('utf-8')}")
    print(f"   🔑 {mk_s.hex()[:16]}... | ✅ sig ok | keys match: {mk_s == mk_r}")

    # msg 2: Bob -> Alice + DH step (new pair in header) / + DH-шаг (новая пара в заголовке)
    bob.dh_step(alice.public(), "send")
    alice.dh_step(bob.public(), "recv")
    mk_s = bob.send_key()
    env = encrypt("Hi Alice! Loud and clear. / Привет, Алиса! Слышу отлично.".encode("utf-8"), mk_s, bob_id)
    mk_r = alice.recv_key()
    plain = decrypt(env, mk_r, b_pub)
    print(f"📨 2. Bob -> Alice: {plain.decode('utf-8')}")
    print(f"   🔑 {mk_s.hex()[:16]}... | ✅ sig ok | keys match: {mk_s == mk_r}")

    # msg 3: Alice -> Bob + DH step / + DH-шаг
    alice.dh_step(bob.public(), "send")
    bob.dh_step(alice.public(), "recv")
    mk_s = alice.send_key()
    env = encrypt("Healed & rotating 🔐 / Лечимся и меняем ключи 🔐".encode("utf-8"), mk_s, alice_id)
    mk_r = bob.recv_key()
    plain = decrypt(env, mk_r, a_pub)
    print(f"📨 3. Alice -> Bob: {plain.decode('utf-8')}")
    print(f"   🔑 {mk_s.hex()[:16]}... | ✅ sig ok | keys match: {mk_s == mk_r}")

    print("✅ Full Double Ratchet in session / полный Double Ratchet в сессии")
    print("🏮 v3: per-message keys + healing / ключ на сообщение + лечение")
