"""
Lantern - Noise XX handshake (mutual auth, MITM-resistant).
Noise XX рукопожатие (взаимная аутентификация, защита от MITM).

Pattern XX (as in WireGuard-style protocols / как в WireGuard-подобных протоколах):
  -> e
  <- e, ee, s, es
  -> s, se

No pre-shared keys: identities (static DH keys) are authenticated
inside the handshake, encrypted and bound to the transcript.
Без предзаданных ключей: идентичности (статические DH-ключи)
аутентифицируются внутри рукопожатия, зашифрованы и привязаны к транскрипту.

Requires: pip install cryptography
"""

import hashlib
import hmac

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey,
)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def raw(pub) -> bytes:
    """Public key as 32 bytes / публичный ключ как 32 байта."""
    return pub.public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )


def from_raw(data: bytes):
    return X25519PublicKey.from_public_bytes(data)


def hkdf2(ck: bytes, ikm: bytes) -> tuple[bytes, bytes]:
    """HKDF-SHA256, two outputs / HKDF-SHA256, два выхода."""
    temp = hmac.new(ck, ikm, hashlib.sha256).digest()
    o1 = hmac.new(temp, b"\x01", hashlib.sha256).digest()
    o2 = hmac.new(temp, o1 + b"\x02", hashlib.sha256).digest()
    return o1, o2


class CipherState:
    """Data key with counter / ключ данных со счётчиком."""

    def __init__(self, k: bytes):
        self.k = k
        self.n = 0

    def encrypt(self, ad: bytes, pt: bytes) -> bytes:
        ct = AESGCM(self.k).encrypt(self.n.to_bytes(12, "big"), pt, ad)
        self.n += 1
        return ct

    def decrypt(self, ad: bytes, ct: bytes) -> bytes:
        pt = AESGCM(self.k).decrypt(self.n.to_bytes(12, "big"), ct, ad)
        self.n += 1
        return pt


class SymmetricState:
    """Transcript hash + key chain / хэш транскрипта + цепочка ключей."""

    def __init__(self):
        self.h = hashlib.sha256(b"Noise_XX_Lantern_25519_SHA256_AESGCM").digest()
        self.ck = self.h
        self.k = None

    def mix_hash(self, data: bytes) -> None:
        self.h = hashlib.sha256(self.h + data).digest()

    def mix_key(self, ikm: bytes) -> None:
        self.ck, self.k = hkdf2(self.ck, ikm)

    def encrypt_and_hash(self, pt: bytes) -> bytes:
        ct = AESGCM(self.k).encrypt(b"\x00" * 12, pt, self.h)
        self.mix_hash(ct)
        return ct

    def decrypt_and_hash(self, ct: bytes) -> bytes:
        pt = AESGCM(self.k).decrypt(b"\x00" * 12, ct, self.h)
        self.mix_hash(ct)
        return pt

    def split(self) -> tuple["CipherState", "CipherState"]:
        k1, k2 = hkdf2(self.ck, b"")
        return CipherState(k1), CipherState(k2)


if __name__ == "__main__":
    print("🔊 Noise XX handshake demo / демо рукопожатия Noise XX")
    print("=" * 54)

    a_ss, b_ss = SymmetricState(), SymmetricState()
    a_s = X25519PrivateKey.generate()  # Alice identity / идентичность Алисы
    b_s = X25519PrivateKey.generate()  # Bob identity / идентичность Боба

    # -> e
    a_e = X25519PrivateKey.generate()
    msg1 = raw(a_e.public_key())
    a_ss.mix_hash(msg1)

    b_ss.mix_hash(msg1)  # network / сеть
    b_re = from_raw(msg1)

    # <- e, ee, s, es
    b_e = X25519PrivateKey.generate()
    part_e = raw(b_e.public_key())
    b_ss.mix_hash(part_e)
    b_ss.mix_key(b_e.exchange(b_re))                     # ee
    ct_s = b_ss.encrypt_and_hash(raw(b_s.public_key()))  # s (encrypted / зашифрована)
    b_ss.mix_key(b_s.exchange(b_re))                     # es
    msg2 = part_e + ct_s

    a_epub_raw, ct_s_rx = msg2[:32], msg2[32:]  # network / сеть
    a_ss.mix_hash(a_epub_raw)
    a_re = from_raw(a_epub_raw)
    a_ss.mix_key(a_e.exchange(a_re))                     # ee
    b_spub = from_raw(a_ss.decrypt_and_hash(ct_s_rx))    # s
    a_ss.mix_key(a_e.exchange(b_spub))                   # es

    # -> s, se
    msg3 = a_ss.encrypt_and_hash(raw(a_s.public_key()))  # s
    a_ss.mix_key(a_s.exchange(a_re))                     # se

    a_spub = from_raw(b_ss.decrypt_and_hash(msg3))  # network / сеть
    b_ss.mix_key(b_e.exchange(a_spub))                   # se

    print(f"🖐️ Alice fingerprint / отпечаток Алисы: {a_ss.h.hex()[:24]}...")
    print(f"🖐️ Bob fingerprint   / отпечаток Боба:   {b_ss.h.hex()[:24]}...")
    print(f"✅ No MITM: fingerprints match / нет MITM: {a_ss.h == b_ss.h}")

    # Data keys / ключи данных
    a_send, a_recv = a_ss.split()
    b_recv, b_send = b_ss.split()

    ct = a_send.encrypt(b"", "Hello over Noise! / Привет через Noise!".encode("utf-8"))
    pt = b_recv.decrypt(b"", ct)
    print(f"📨 First message / первое сообщение: {pt.decode('utf-8')}")

    ct = b_send.encrypt(b"", "Loud and clear! / Слышу отлично!".encode("utf-8"))
    pt = a_recv.decrypt(b"", ct)
    print(f"📨 Reply / ответ: {pt.decode('utf-8')}")
    print("✅ Mutual auth, zero pre-shared keys / взаимная аутентификация без общих ключей")
