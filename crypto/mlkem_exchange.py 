"""
Lantern - ML-KEM-768 key exchange prototype.
Прототип обмена ключами ML-KEM-768.

Post-quantum KEM (NIST FIPS 203): keygen -> encaps -> decaps.
Постквантовый KEM: генерация -> инкапсуляция -> декапсуляция.

Requires: pip install kyber-py
"""

from kyber_py.ml_kem import ML_KEM_768


def key_exchange_demo():
    """Alice and Bob derive a shared secret / Алиса и Боб выводят общий секрет."""
    ek, dk = ML_KEM_768.keygen()          # Alice / Алиса
    bob_key, ct = ML_KEM_768.encaps(ek)   # Bob / Боб
    alice_key = ML_KEM_768.decaps(dk, ct) # Alice / Алиса
    return alice_key, bob_key


if __name__ == "__main__":
    a, b = key_exchange_demo()
    print(f"🔑 Alice key / ключ Алисы: {a.hex()[:32]}...")
    print(f"🔑 Bob key   / ключ Боба:   {b.hex()[:32]}...")
    print(f"✅ Shared secret matches / общий секрет совпадает: {a == b}")
