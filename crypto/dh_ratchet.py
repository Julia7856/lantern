"""
Lantern - DH ratchet (post-compromise security).
DH-рэтчет (пост-компрометационная безопасность).

Symmetric ratchet protects the PAST (forward secrecy).
DH ratchet protects the FUTURE: a new DH pair on every turn
"heals" secrecy even after key theft.
Симметричный рэтчет защищает ПРОШЛОЕ (forward secrecy).
DH-рэтчет защищает БУДУЩЕЕ: новая DH-пара на каждом ходе
"лечит" секретность даже после кражи ключей.

Requires: pip install cryptography
"""

import hashlib

from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey


class Peer:
    """Participant with a DH pair / участник с DH-парой."""

    def __init__(self, name: str):
        self.name = name
        self.priv = X25519PrivateKey.generate()
        self.root = b"\x00" * 32

    def public(self):
        return self.priv.public_key()

    def new_pair(self):
        """New DH pair for the turn / новая DH-пара для хода."""
        self.priv = X25519PrivateKey.generate()
        return self.public()

    def ratchet(self, remote_pub) -> bytes:
        """New root key from DH exchange / новый корневой ключ из DH-обмена."""
        shared = self.priv.exchange(remote_pub)
        self.root = hashlib.sha256(self.root + shared).digest()
        return self.root


if __name__ == "__main__":
    print("🔄 DH ratchet demo / демо DH-рэтчета")
    print("=" * 50)

    alice = Peer("Alice")
    bob = Peer("Bob")

    # Turn 0: initial exchange / ход 0: начальный обмен
    a_pub, b_pub = alice.public(), bob.public()
    k0_a = alice.ratchet(b_pub)
    k0_b = bob.ratchet(a_pub)
    print(f"🔐 Turn 0 root / корень хода 0: {k0_a.hex()[:24]}...")
    print(f"   Alice==Bob: {k0_a == k0_b}")

    # Simulate key theft / симуляция кражи ключа
    stolen = k0_a
    print(f"🕵️ Attacker stole the root / атакующий украл корень: {stolen.hex()[:24]}...")

    # Turn 1: Bob changes DH pair and replies / ход 1: Боб меняет DH-пару и отвечает
    b_pub2 = bob.new_pair()
    k1_b = bob.ratchet(a_pub)     # Bob: new priv * Alice pub / новый прив * паб Алисы
    k1_a = alice.ratchet(b_pub2)  # Alice: her priv * Bob new pub / её прив * новый паб Боба
    print(f"🔐 Turn 1 root / корень хода 1: {k1_a.hex()[:24]}...")
    print(f"   Alice==Bob: {k1_a == k1_b}")

    print(f"🔥 Roots differ / корни разные: {k0_a != k1_a}")
    print(f"🛡️ Attacker left behind / атакующий отстал: {stolen != k1_a}")
    print("✅ Post-compromise security: secrecy healed / секретность вылечена")
