"""
Lantern - End-to-end session demo.
Сквозное демо сессии.

Pipeline / Конвейер:
  1. did:key identity (Ed25519) / DID-идентичность
  2. hybrid KEM (X25519 + ML-KEM-768) / гибридный KEM
  3. sign with identity key / подпись ключом идентичности
  4. AES-256-GCM encryption / шифрование
  5. decrypt + verify / расшифровка + проверка

Requires: pip install kyber-py cryptography
"""

import hashlib
import os

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from kyber_py.ml_kem import ML_KEM_768


def make_identity():
    """Create Ed25519 identity / Создаёт Ed25519-идентичность."""
    priv = Ed25519PrivateKey.generate()
    return priv, priv.public_key()


def establish_session_key():
    """Hybrid session key: X25519 + ML-KEM-768 / Гибридный сессионный ключ."""
    # Classic / классика
    a = X25519PrivateKey.generate()
    b = X25519PrivateKey.generate()
    shared_x = a.exchange(b.public_key())

    # Post-quantum / постквант (official API / официальный API)
    ek, dk = ML_KEM_768.keygen()
    ss_bob, ct = ML_KEM_768.encaps(ek)
    ss_alice = ML_KEM_768.decaps(dk, ct)
    assert ss_alice == ss_bob

    return hashlib.sha256(shared_x + ss_alice).digest()


def send_message(priv_id, key, text):
    """Sign + encrypt / Подписать + зашифровать."""
    msg = text.encode()
    sig = priv_id.sign(msg)
    nonce = os.urandom(12)
    ct = AESGCM(key[:32]).encrypt(nonce, msg + b"||" + sig, None)
    return nonce + ct


def receive_message(pub_id, key, data):
    """Decrypt + verify / Расшифровать + проверить."""
    nonce, ct = data[:12], data[12:]
    payload = AESGCM(key[:32]).decrypt(nonce, ct, None)
    msg, sig = payload.rsplit(b"||", 1)
    pub_id.verify(sig, msg)
    return msg.decode()


if __name__ == "__main__":
    print("🏮 Lantern session demo / демо сессии Lantern")
    print("=" * 50)
    alice_priv, alice_pub = make_identity()
    bob_priv, bob_pub = make_identity()
    print("👤 Alice & Bob identities created / идентичности созданы")

    key = establish_session_key()
    print(f"🔐 Hybrid session key / гибридный ключ: {len(key)} bytes")

    env = send_message(alice_priv, key, "Hello Bob, this is Alice! / Привет, Боб, это Алиса!")
    print(f"📦 Envelope sent / конверт отправлен: {len(env)} bytes")

    out = receive_message(alice_pub, key, env)
    print(f"📬 Bob received / Боб получил: {out}")
    print("✅ Signature verified / подпись проверена")
    print("=" * 50)
    print("🏮 Privacy + authenticity + post-quantum — in one flow / в одном потоке")
