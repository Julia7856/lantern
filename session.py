"""
Lantern - End-to-end session demo.
Сквозное демо сессии.

Alice -> Bob: identity + hybrid key + signed encrypted message.
Алиса -> Боб: идентичность + гибридный ключ + подписанное зашифрованное сообщение.

Pipeline / Конвейер:
  1. did:key identity / DID-идентичность
  2. hybrid KEM (X25519 + ML-KEM-768) / гибридный KEM
  3. sign message with identity key / подпись сообщения ключом идентичности
  4. AES-256-GCM encryption / шифрование AES-256-GCM
  5. decrypt + verify signature / расшифровка + проверка подписи

Requires: pip install kyber-py cryptography
"""

import hashlib
import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidSignature

from kyber import ML_KEM_768 as kem


# ---- 1. Identity: did:key (Ed25519) / Идентичность: did:key ----

def make_identity():
    """Create Ed25519 identity / Создаёт Ed25519-идентичность."""
    private = Ed25519PrivateKey.generate()
    public = private.public_key()
    return private, public


# ---- 2. Hybrid KEM: X25519 + ML-KEM-768 / Гибридный KEM ----

def establish_session_key():
    """Establish a hybrid session key / Устанавливает гибридный сессионный ключ."""
    # Classic X25519 / Классический X25519
    priv_x_a = X25519PrivateKey.generate()
    pub_x_a = priv_x_a.public_key()
    priv_x_b = X25519PrivateKey.generate()
    pub_x_b = priv_x_b.public_key()
    shared_x = priv_x_a.exchange(pub_x_b)

    # Post-quantum ML-KEM-768 / Постквантовый ML-KEM-768
    pk, sk = kem.generate_keypair()
    ct, ss_b = kem.encapsulate(pk)
    ss_a = kem.decapsulate(ct, sk)
    assert ss_a == ss_b

    # Combine / Комбинация
    return hashlib.sha256(shared_x + ss_a).digest()


# ---- 3 & 4. Sign + encrypt / Подпись + шифрование ----

def send_message(private_id, session_key, plaintext: str) -> bytes:
    """Sign with identity, encrypt with session key /
    Подписать ключом идентичности, зашифровать сессионным ключом."""
    message = plaintext.encode("utf-8")

    # Sign / Подпись
    signature = private_id.sign(message)

    # Encrypt (message + signature) / Шифрование (сообщение + подпись)
    nonce = os.urandom(12)
    aesgcm = AESGCM(session_key[:32])
    payload = message + b"||" + signature  # simple delimiter / простой разделитель
    ciphertext = aesgcm.encrypt(nonce, payload, None)
    return nonce + ciphertext


# ---- 5. Decrypt + verify / Расшифровка + проверка ----

def receive_message(public_id, session_key, data: bytes) -> str:
    """Decrypt, then verify the signature /
    Расшифровать, затем проверить подпись."""
    nonce, ciphertext = data[:12], data[12:]
    aesgcm = AESGCM(session_key[:32])
    payload = aesgcm.decrypt(nonce, ciphertext, None)

    message, signature = payload.rsplit(b"||", 1)
    try:
        public_id.verify(signature, message)
    except InvalidSignature as e:
        raise ValueError("Signature invalid / Подпись не верна") from e

    return message.decode("utf-8")


# ---- Demo / Демо ----

if __name__ == "__main__":
    print("🏮 Lantern session demo / демо сессии Lantern")
    print("=" * 50)

    # Alice and Bob create identities / Алиса и Боб создают идентичности
    alice_priv, alice_pub = make_identity()
    bob_priv, bob_pub = make_identity()
    print("👤 Alice identity created / идентичность Алисы создана")
    print("👤 Bob identity created / идентичность Боба создана")

    # They establish a hybrid session key / Они устанавливают гибридный ключ
    session_key = establish_session_key()
    print(f"🔐 Hybrid session key established / гибридный сессионный ключ установлен ({len(session_key)} bytes)")

    # Alice sends Bob a signed, encrypted message /
    # Алиса отправляет Бобу подписанное зашифрованное сообщение
    text = "Hello Bob, this is Alice! / Привет, Боб, это Алиса!"
    envelope = send_message(alice_priv, session_key, text)
    print(f"📦 Envelope sent / конверт отправлен ({len(envelope)} bytes)")

    # Bob receives, decrypts, verifies / Боб получает, расшифровывает, проверяет
    received = receive_message(alice_pub, session_key, envelope)
    print(f"📬 Bob received / Боб получил: {received}")
    print("✅ Signature verified by Bob / Подпись проверена Бобом")
    print("=" * 50)
    print("🏮 Privacy, authenticity, and post-quantum protection — in one flow.")
    print("   Приватность, аутентичность и постквантовая защита — в одном потоке.")
