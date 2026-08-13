"""
Lantern - DID identity prototype (did:key, Ed25519).
Прототип DID-идентичности (did:key, Ed25519).

Self-sovereign identity: no server, no registry, no passport.
Identifier is derived from the public key itself (W3C DID).
Самосуверенная идентичность: без сервера, без реестра, без паспорта.
Идентификатор выводится из самого публичного ключа (W3C DID).

Requires: pip install cryptography
"""

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# base58btc alphabet (Bitcoin-style) / алфавит base58btc
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def base58btc(data: bytes) -> str:
    """Encode bytes to base58btc / Кодирование в base58btc."""
    n = int.from_bytes(data, "big")
    out = []
    while n > 0:
        n, r = divmod(n, 58)
        out.append(B58[r])
    for b in data:  # leading zeros / ведущие нули
        if b == 0:
            out.append("1")
        else:
            break
    return "".join(reversed(out))


def create_did() -> dict:
    """Create a did:key identity / Создаёт did:key идентичность."""
    # 1. Ed25519 keypair / пара ключей
    private_key = Ed25519PrivateKey.generate()
    pub_raw = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    # 2. multicodec prefix for ed25519-pub: 0xed 0x01
    prefixed = bytes([0xED, 0x01]) + pub_raw

    # 3. multibase base58btc ('z') -> did:key
    did = "did:key:z" + base58btc(prefixed)

    return {"did": did, "private_key": private_key, "public_key_raw": pub_raw}


def sign_message(private_key, message: bytes) -> bytes:
    """Sign with identity key / Подписать ключом идентичности."""
    return private_key.sign(message)


def verify_message(public_key, signature: bytes, message: bytes) -> bool:
    """Verify signature / Проверить подпись."""
    try:
        public_key.verify(signature, message)
        return True
    except InvalidSignature:
        return False


if __name__ == "__main__":
    identity = create_did()
    print(f"🪪 Your DID / твой DID: {identity['did']}")

    msg = b"Hello from Lantern / Привет от Lantern"
    sig = sign_message(identity["private_key"], msg)
    print(f"✍️ Signature / подпись: {sig.hex()[:64]}...")

    ok = verify_message(identity["private_key"].public_key(), sig, msg)
    print(f"✅ Signature valid / подпись верна: {ok}")
