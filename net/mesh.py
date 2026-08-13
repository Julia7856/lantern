"""
Lantern - P2P mesh transport prototype (store-and-forward).
Прототип P2P mesh-транспорта (store-and-forward).

E2E-encrypted envelopes hop through untrusted relays.
Relays see only ciphertext: compromised transport != compromised content.
E2E-зашифрованные конверты прыгают через недоверенные реле.
Реле видят только шифртекст: скомпрометированный транспорт != скомпрометированное содержимое.

Pure simulation, no real network / чистая симуляция, без реальной сети.

Requires: pip install cryptography
"""

import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Node:
    """Mesh node / узел mesh-сети."""

    def __init__(self, name: str):
        self.name = name
        self.peers: list["Node"] = []
        self.inbox: list[tuple[bytes, bytes]] = []

    def link(self, other: "Node") -> None:
        """Bidirectional link / двунаправленная связь."""
        self.peers.append(other)
        other.peers.append(self)

    def relay(self, dst: str, nonce: bytes, ct: bytes, came_from: "Node | None" = None) -> None:
        """Forward the envelope / передать конверт дальше."""
        if self.name == dst:
            self.inbox.append((nonce, ct))
            print(f"   📬 {self.name}: envelope delivered / конверт доставлен")
            return
        print(f"   🔀 {self.name}: relays {len(ct)} bytes (ciphertext only / только шифртекст)")
        for p in self.peers:
            if p is not came_from:
                p.relay(dst, nonce, ct, self)
                return


if __name__ == "__main__":
    print("🕸️ Mesh transport demo / демо mesh-транспорта")
    print("=" * 50)

    # Chain of untrusted relays / цепочка недоверенных реле
    alice, r1, r2, bob = Node("Alice"), Node("R1"), Node("R2"), Node("Bob")
    alice.link(r1)
    r1.link(r2)
    r2.link(bob)

    # E2E key (in reality - from Double Ratchet) / E2E-ключ (в реальности - из Double Ratchet)
    e2e = os.urandom(32)
    nonce = os.urandom(12)
    ct = AESGCM(e2e).encrypt(nonce, "Hello over the mesh! / Привет через mesh!".encode("utf-8"), None)

    print(f"📤 Alice sends {len(ct)} bytes via R1->R2 / Алиса шлёт через R1->R2")
    alice.relay("Bob", nonce, ct)

    print(f"🕵️ R1 sees / R1 видит: {ct.hex()[:32]}... (no key - no meaning / нет ключа - нет смысла)")

    nonce_b, ct_b = bob.inbox[0]
    plain = AESGCM(e2e).decrypt(nonce_b, ct_b, None)
    print(f"📥 Bob reads / Боб читает: {plain.decode('utf-8')}")
    print("✅ E2E survives untrusted relays / E2E переживает недоверенные реле")
