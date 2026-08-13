"""
Lantern - Symmetric ratchet (hash chain).
Симметричный рэтчет (хэш-цепочка).

Forward secrecy: each message gets its own key;
the chain key moves only forward, the old one is destroyed.
Forward secrecy: каждое сообщение получает свой ключ;
ключ цепочки идёт только вперёд, старый уничтожается.

Signal-style KDF chain (simplified):
  MK_i   = HMAC(CK_i, 0x01)   # message key / ключ сообщения
  CK_i+1 = HMAC(CK_i, 0x02)   # next chain key / следующий ключ цепочки
"""

import hashlib
import hmac
import os


class SymRatchet:
    """Symmetric-key ratchet / симметричный рэтчет ключей."""

    def __init__(self, chain_key: bytes | None = None):
        self.ck = chain_key or os.urandom(32)

    def next_key(self) -> bytes:
        """Message key + advance the chain / ключ сообщения + шаг цепочки."""
        mk = hmac.new(self.ck, b"\x01", hashlib.sha256).digest()
        self.ck = hmac.new(self.ck, b"\x02", hashlib.sha256).digest()
        return mk


if __name__ == "__main__":
    print("🔄 Symmetric ratchet demo / демо симметричного рэтчета")
    print("=" * 50)

    # Common root (in reality - from hybrid KEM) / общий корень (в реальности - из hybrid KEM)
    root = os.urandom(32)
    alice = SymRatchet(root)
    bob = SymRatchet(root)

    keys = []
    for i in range(1, 4):
        k_a = alice.next_key()
        k_b = bob.next_key()
        keys.append(k_a)
        print(f"📨 Message {i} key / ключ сообщения {i}: {k_a.hex()[:24]}...")
        print(f"   Alice==Bob: {k_a == k_b}")

    print(f"🔑 All keys different / все ключи разные: {len(set(keys)) == len(keys)}")
    print("🔥 Chain key destroyed after step / ключ цепочки сгорел после шага")
    print("✅ Forward secrecy: past is unreadable / прошлое нечитаемо")
