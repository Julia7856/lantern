"""
Lantern - Double Ratchet state (Signal-style).
Состояние Double Ratchet (как в Signal).

Combines:
  - DH ratchet: new root on every turn (heals future)
  - Symmetric ratchet: new key per message (hides past)
Объединяет:
  - DH-рэтчет: новый корень на каждом ходе (лечит будущее)
  - симметричный рэтчет: новый ключ на сообщение (прячет прошлое)

Requires: pip install cryptography
"""

import hashlib
import hmac

from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey


class DoubleRatchet:
    """Per-peer ratchet state / состояние рэтчета для каждого собеседника."""

    def __init__(self, name: str):
        self.name = name
        self.priv = X25519PrivateKey.generate()
        self.root = b"\x00" * 32
        self.send_chain = None
        self.recv_chain = None

    @staticmethod
    def _step(chain_key: bytes) -> tuple[bytes, bytes]:
        """Message key + next chain key / ключ сообщения + следующий ключ цепочки."""
        mk = hmac.new(chain_key, b"\x01", hashlib.sha256).digest()
        nk = hmac.new(chain_key, b"\x02", hashlib.sha256).digest()
        return mk, nk

    def public(self):
        return self.priv.public_key()

    def init_as_sender(self, remote_pub) -> None:
        """Alice: init with Bob's public key / Алиса: старт с публичным ключом Боба."""
        shared = self.priv.exchange(remote_pub)
        self.root = hashlib.sha256(self.root + shared).digest()
        self.send_chain = self.root

    def init_as_receiver(self, remote_pub) -> None:
        """Bob: init with Alice's public key / Боб: старт с публичным ключом Алисы."""
        shared = self.priv.exchange(remote_pub)
        self.root = hashlib.sha256(self.root + shared).digest()
        self.recv_chain = self.root

    def send_key(self) -> bytes:
        mk, self.send_chain = self._step(self.send_chain)
        return mk

    def recv_key(self) -> bytes:
        mk, self.recv_chain = self._step(self.recv_chain)
        return mk

    def dh_step(self, remote_pub, direction: str) -> None:
        """DH ratchet step / шаг DH-рэтчета.

        send: new DH pair (healing) + new send chain.
        recv: keep own pair, adopt remote's new key + new recv chain.
        send: новая DH-пара (лечение) + новая цепочка отправки.
        recv: своя пара остаётся, принимаем новый ключ + новая цепочка приёма.
        """
        if direction == "send":
            self.priv = X25519PrivateKey.generate()
        shared = self.priv.exchange(remote_pub)
        self.root = hashlib.sha256(self.root + shared).digest()
        if direction == "send":
            self.send_chain = self.root
        else:
            self.recv_chain = self.root


if __name__ == "__main__":
    print("🧬 Double Ratchet state demo / демо состояния Double Ratchet")
    print("=" * 54)

    alice = DoubleRatchet("Alice")
    bob = DoubleRatchet("Bob")

    alice.init_as_sender(bob.public())
    bob.init_as_receiver(alice.public())

    ka = alice.send_key()
    kb = bob.recv_key()
    print(f"📨 A->B 1: {ka.hex()[:16]}... match: {ka == kb}")

    # Bob replies: send-step for Bob, recv-step for Alice / Боб отвечает: send-шаг у Боба, recv-шаг у Алисы
    bob.dh_step(alice.public(), "send")
    alice.dh_step(bob.public(), "recv")
    kb = bob.send_key()
    ka = alice.recv_key()
    print(f"📨 B->A 1: {kb.hex()[:16]}... match: {ka == kb}")

    # Alice again / снова Алиса
    alice.dh_step(bob.public(), "send")
    bob.dh_step(alice.public(), "recv")
    ka = alice.send_key()
    kb = bob.recv_key()
    print(f"📨 A->B 2: {ka.hex()[:16]}... match: {ka == kb}")

    print("✅ Double Ratchet ping-pong works / пинг-понг работает")
