"""
Lantern - Hybrid Key Exchange (Defense in Depth).
Гибридный обмен ключами (Эшелонированная защита).

Если квантовый компьютер сломает X25519, ML-KEM-768 устоит.
Если в ML-KEM найдут математическую ошибку, X25519 устоит.
Стандарт индустрии (Signal, TLS 1.3) / Industry standard.

Requires: pip install kyber-py cryptography
"""

import hashlib
from kyber import ML_KEM_768 as kem
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey


def hybrid_key_exchange():
    """Гибридный обмен: классика + постквант / Hybrid: classic + PQ."""
    
    print("🔄 Инициализация Алисы и Боба / Initializing Alice and Bob...")

    # 1. Классический ECDH (X25519) / Classic ECDH
    priv_x_alice = X25519PrivateKey.generate()
    pub_x_alice = priv_x_alice.public_key()
    
    priv_x_bob = X25519PrivateKey.generate()
    pub_x_bob = priv_x_bob.public_key()
    
    # Классический общий секрет / Classic shared secret
    shared_x = priv_x_alice.exchange(pub_x_bob)
    
    # 2. Постквантовый ML-KEM / Post-quantum ML-KEM
    pk_a, sk_a = kem.generate_keypair()
    ct, shared_pq_bob = kem.encapsulate(pk_a)
    shared_pq_alice = kem.decapsulate(ct, sk_a)
    
    # 3. Комбинация секретов (Стандарт NIST) / Combining secrets (NIST standard)
    # Конкатенация и хэширование / Concatenation and hashing
    combined_secret = shared_x + shared_pq_alice
    session_key = hashlib.sha256(combined_secret).digest()
    
    print("-" * 40)
    print(f"🔒 Classic secret (X25519): {len(shared_x)} bytes")
    print(f"🧬 Post-Quantum secret (ML-KEM): {len(shared_pq_alice)} bytes")
    print(f"✨ Hybrid Session Key (SHA-256): {session_key.hex()}")
    print("-" * 40)
    print("✅ Двойная защита установлена / Double protection established!")


if __name__ == "__main__":
    hybrid_key_exchange()
