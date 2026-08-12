"""
Lantern - Post-quantum key exchange prototype.
Прототип постквантового обмена ключами.

ML-KEM-768 (NIST FIPS 203, formerly Kyber768).
Pure Python: pip install kyber-py

Education & honest security research /
Образование и честные исследования безопасности.
"""

from kyber import ML_KEM_768 as kem


def key_exchange() -> bytes:
    """Полный цикл ML-KEM-768 / Full ML-KEM-768 cycle."""

    # 1. Алиса создаёт пару ключей / Alice generates a keypair
    pk_a, sk_a = kem.generate_keypair()
    print(f"🔑 Public key / публичный ключ: {len(pk_a)} bytes")
    print(f"🗝️ Secret key / секретный ключ: {len(sk_a)} bytes")

    # 2. Боб инкапсулирует общий секрет / Bob encapsulates the shared secret
    ciphertext, ss_bob = kem.encapsulate(pk_a)
    print(f"📦 Ciphertext / шифртекст: {len(ciphertext)} bytes")

    # 3. Алиса декапсулирует / Alice decapsulates
    ss_alice = kem.decapsulate(ciphertext, sk_a)

    # 4. Проверка / check
    assert ss_alice == ss_bob, "Secrets differ / секреты не совпадают!"
    print("✅ Shared secret established / общий секрет установлен")
    print(f"🤫 Shared secret / общий секрет: {len(ss_alice)} bytes")
    return ss_alice


if __name__ == "__main__":
    key_exchange()
