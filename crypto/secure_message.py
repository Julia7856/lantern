"""
Lantern - Secure message encryption with hybrid session key.
Шифрование сообщений гибридным сессионным ключом.

Hybrid session key -> AES-256-GCM -> ciphertext.
Наследие Grail: проверенный AEAD / Grail heritage: proven AEAD.

Requires: pip install cryptography
"""

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_message(session_key: bytes, plaintext: str) -> bytes:
    """Шифрует сообщение / Encrypts a message."""
    aes_key = session_key[:32]  # AES-256 требует 32 байта / needs 32 bytes
    nonce = os.urandom(12)  # 96-битный nonce для GCM / 96-bit nonce for GCM
    aesgcm = AESGCM(aes_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    return nonce + ciphertext  # nonce едет вместе с шифртекстом / nonce travels with ciphertext


def decrypt_message(session_key: bytes, data: bytes) -> str:
    """Расшифровывает сообщение / Decrypts a message."""
    aes_key = session_key[:32]
    nonce, ciphertext = data[:12], data[12:]
    aesgcm = AESGCM(aes_key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode("utf-8")


if __name__ == "__main__":
    # Демо: сессионный ключ как из hybrid_kem / Demo: session key as from hybrid_kem
    import hashlib
    demo_key = hashlib.sha256(b"demo shared secret").digest()

    msg = "Приватность — это право, а не функция / Privacy is a right, not a feature"
    sealed = encrypt_message(demo_key, msg)
    print(f"📦 Ciphertext / шифртекст: {sealed.hex()}")

    opened = decrypt_message(demo_key, sealed)
    print(f"📬 Decrypted / расшифровано: {opened}")
