"""
Lantern - end-to-end session demo v2 (with ratchet).
Демо сквозной сессии v2 (с рэтчетом).

did:key identity + hybrid KEM (X25519 + ML-KEM-768) + AES-256-GCM +
Ed25519 signature + symmetric ratchet: each message on its own key.
did:key идентичность + гибридный KEM (X25519 + ML-KEM-768) + AES-256-GCM +
подпись Ed25519 + симметричный рэтчет: каждое сообщение на своём ключе.

Requires: pip install kyber-py cryptography
"""

import hashlib
import os

from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from kyber_py.ml_kem import ML_KEM_768

from crypto.ratchet import SymRatchet
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


def send(text: bytes, mk: bytes, sender: dict) -> dict:
    """Encrypt + sign / зашифровать + подписать."""
    nonce = os.urandom(12)
    ct = AESGCM(mk).encrypt(nonce, text, None)
    sig = sign_message(sender["private_key"], ct)
    return {"nonce": nonce, "ct": ct, "sig": sig}


def recv(env: dict, mk: bytes, sender_pub) -> bytes:
    """Verify + decrypt / проверить подпись + расшифровать."""
    assert verify_message(sender_pub, env["sig"], env["ct"])
    return AESGCM(mk).decrypt(env["nonce"], env["ct"], None)


if __name__ == "__main__":
    print("🏮 Lantern session demo v2 / демо сессии Lantern v2")
    print("=" * 56)

    # 1. Identities / идентичности
    alice = create_did()
    bob = create_did()
    print("👤 Alice & Bob identities created / идентичности созданы")

    # 2. Hybrid root key / гибридный корневой ключ
    root = hybrid_session_key()
    print(f"🔐 Hybrid session key / гибридный ключ: {len(root)} bytes")

    # 3. Ratchet chains per direction / цепочки рэтчета на каждое направление
    ab_root = hashlib.sha256(root + b"alice->bob").digest()
    ba_root = hashlib.sha256(root + b"bob->alice").digest()
    ab_send, ab_recv = SymRatchet(ab_root), SymRatchet(ab_root)
    ba_send, ba_recv = SymRatchet(ba_root), SymRatchet(ba_root)

    # 4. Three messages, each on its own key / три сообщения, каждое на своём ключе
    flow = [
        ("alice", "Hello Bob, this is Alice! / Привет, Боб, это Алиса!"),
        ("bob", "Hi Alice! Loud and clear. / Привет, Алиса! Слышу отлично."),
        ("alice", "Keys rotate every message 🔐 / Ключи меняются с каждым сообщением 🔐"),
    ]

    keys_seen = []
    for i, (who, text) in enumerate(flow, 1):
        if who == "alice":
            s_chain, r_chain, sender = ab_send, ab_recv, alice
            label = "Alice -> Bob"
        else:
            s_chain, r_chain, sender = ba_send, ba_recv, bob
            label = "Bob -> Alice"

        mk_s = s_chain.next_key()
        env = send(text.encode("utf-8"), mk_s, sender)
        mk_r = r_chain.next_key()
        plain = recv(env, mk_r, sender["private_key"].public_key())
        keys_seen.append(mk_s)

        print(f"📨 {i}. {label}: {plain.decode('utf-8')}")
        print(f"   🔑 {mk_s.hex()[:16]}... | ✅ sig ok | keys match: {mk_s == mk_r}")

    print(f"🔑 All message keys different / все ключи разные: {len(set(keys_seen)) == len(keys_seen)}")
    print("✅ Forward secrecy inside session / forward secrecy внутри сессии")
    print("=" * 56)
    print("🏮 v2: ratchet engaged / рэтчет задействован")
