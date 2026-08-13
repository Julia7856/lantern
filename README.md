# 🏮 Lantern

**Post-quantum private P2P communicator / Приватный P2P-коммуникатор с постквантовой криптографией и mesh-сетью**

> Relative privacy on the network / Относительная приватность в сети.

## 🎯 What is this? / Что это?

Lantern — децентрализованный коммуникатор: без телефона, без паспорта,
без центрального сервера / a decentralized communicator: no phone, no passport,
no central server.

- 🧬 **Post-quantum / Постквантовая криптография**: ML-KEM-768 (NIST FIPS 203)
- 🕸️ **Mesh / Mesh-сеть**: Bluetooth / Wi-Fi Direct / LoRa + anonymous overlay fallback
- 🪪 **DID / Децентрализованная идентичность**: W3C did:key, без личных данных
- 📴 **Offline-first / Офлайн-первичность**: работает без интернета
- 🔒 **E2E by default / E2E по умолчанию**: hybrid ML-KEM + X25519 → AES-256-GCM

## 📁 Structure / Структура

- `crypto/mlkem_exchange.py` — ML-KEM-768 key exchange / обмен ключами
- `crypto/hybrid_kem.py` — hybrid KEM (X25519 + ML-KEM) / гибридный KEM
- `crypto/secure_message.py` — AES-256-GCM encryption / шифрование сообщений
- `identity/did_key.py` — did:key identity (Ed25519) / DID-идентичность
- `THREAT_MODEL.md` — honest threat model / честная модель угроз

## 🚧 Status / Статус

Early prototype / Ранний прототип.

- [x] ML-KEM-768 key exchange prototype / прототип обмена ключами
- [x] Hybrid KEM (ML-KEM + X25519) / гибридный KEM
- [x] AES-256-GCM message encryption / шифрование сообщений
- [x] DID identity (did:key, Ed25519) / DID-идентичность
- [x] THREAT_MODEL.md (10 threats + roadmap / 10 угроз + план усиления)
- [ ] End-to-end session demo / сквозное демо сессии
- [ ] P2P transport / P2P-транспорт
- [ ] Double Ratchet / двойной ратчет
- [ ] Mobile UI / мобильный UI

## 🛡️ Threat model / Модель угроз

See / см. [THREAT_MODEL.md](THREAT_MODEL.md)

## ⚖️ Ethics / Этика

Lantern is a privacy protection tool / Lantern — инструмент защиты приватности.
Responsibility for use lies with the user / ответственность за использование — на
пользователе.

For people who value privacy / для людей, которые ценят приватность.
White-hat only / только white-hat.

---

**Made with ❤️ for people who value privacy / Сделано с ❤️ для людей, которые ценят приватность**
