"""
Lantern - Hybrid KEM (X25519 + ML-KEM-768).
Гибридный KEM: классика + постквант.

If one breaks, the other holds / если один сломается, второй устоит.

Requires: pip install kyber-py cryptography
"""

import hashlib

from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey

from kyber_py.ml_kem import ML_KEM_768


def establish_shared_key():
    """Derive a combined shared key / выводит комбинированный общий ключ."""
    # Classic / классика
    a = X25519PrivateKey.generate()
    b = X25519PrivateKey.generate()
    x_shared = a.exchange(b.public_key())

    # Post-quantum / постквант
    ek, dk = ML_KEM_768.keygen()
    k_bob, ct = ML_KEM_768.encaps(ek)
    k_alice = ML_KEM_768.decaps(dk, ct)
    assert k_alice == k_bob

    # Combine / комбинация
    return hashlib.sha256(x_shared + k_alice).digest()


if __name__ == "__main__":
    key = establish_shared_key()
    print(f"🔐 Hybrid shared key / гибридный общий ключ: {len(key)} bytes")
    print("✅ Double lock engaged / двойной замок задействован")
