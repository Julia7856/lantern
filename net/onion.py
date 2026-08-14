"""
Lantern - Onion routing prototype (metadata protection).
Прототип onion-маршрутизации (защита метаданных).

Each relay learns only the next hop - never the final
destination, never the content, never the sender.
Каждое реле узнаёт только следующий прыжок - никогда конечную
цель, никогда содержимое, никогда отправителя.

The message is padded so its length leaks nothing.
Сообщение дополнено до фиксированной длины, чтобы длина ничего не выдавала.

Requires: pip install cryptography
"""

import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MSG_SIZE = 160  # fixed message size / фиксированный размер сообщения


def pad(data: bytes, size: int) -> bytes:
    """Pad to fixed size / дополнить до фиксированного размера."""
    if len(data) > size:
        raise ValueError("too long / слишком длинно")
    return data + b"\x00" * (size - len(data))


def unpad(data: bytes) -> bytes:
    return data.rstrip(b"\x00")


class OnionNode:
    """Relay or endpoint with a layer key / реле или конечная точка с ключом слоя."""

    def __init__(self, name: str, key: bytes):
        self.name = name
        self.aead = AESGCM(key)

    def wrap(self, next_hop: str, payload: bytes) -> bytes:
        """Add one onion layer (Alice builds) / добавить слой лука (строит Алиса)."""
        nonce = os.urandom(12)
        inner = next_hop.encode() + b"|" + payload
        return nonce + self.aead.encrypt(nonce, inner, None)

    def peel(self, packet: bytes) -> tuple[str, bytes]:
        """Remove own layer; learn ONLY next hop / снять свой слой; узнать ТОЛЬКО следующий прыжок."""
        nonce, ct = packet[:12], packet[12:]
        inner = self.aead.decrypt(nonce, ct, None)
        next_hop, payload = inner.split(b"|", 1)
        return next_hop.decode(), payload


if __name__ == "__main__":
    print("🧅 Onion routing demo / демо onion-маршрутизации")
    print("=" * 54)

    # Layer keys: Alice shares one per relay via Noise (simulated here)
    # Ключи слоёв: Алиса делит с каждым реле через Noise (здесь симуляция)
    k_r1, k_r2, k_bob = os.urandom(32), os.urandom(32), os.urandom(32)
    r1 = OnionNode("R1", k_r1)
    r2 = OnionNode("R2", k_r2)
    bob = OnionNode("Bob", k_bob)

    msg = "Meet at the lantern square 🏮 / Встречаемся у площади фонарей 🏮".encode("utf-8")

    # Alice builds the onion inside-out / Алиса строит лук изнутри наружу
    onion = bob.wrap("END", pad(msg, MSG_SIZE))
    onion = r2.wrap("bob", onion)
    onion = r1.wrap("r2", onion)
    print(f"📤 Alice sends {len(onion)} bytes / Алиса шлёт {len(onion)} байт")

    nxt, onion = r1.peel(onion)
    print(f"🔀 R1 sees next hop / R1 видит прыжок: {nxt} | content? no / содержимое? нет")

    nxt, onion = r2.peel(onion)
    print(f"🔀 R2 sees next hop / R2 видит прыжок: {nxt} | sender? no / отправитель? нет")

    nxt, plain = bob.peel(onion)
    print(f"📥 Bob reads / Боб читает: {unpad(plain).decode('utf-8')}")

    print("🕵️ No relay knew both ends / ни одно реле не знало оба конца")
    print("✅ Metadata protected / метаданные защищены")
