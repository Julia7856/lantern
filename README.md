# 🏮 Lantern

**Post-quantum private P2P communicator / Приватный P2P-коммуникатор с постквантовой криптографией и mesh-сетью**

> Privacy is a right, not a feature.
> Приватность — это право, а не функция.

## 🎯 Что это? / What is this?

Lantern — децентрализованный коммуникатор: без телефона, без паспорта,
без центрального сервера / a decentralized communicator: no phone, no passport,
no central server.

- 🧬 **Post-quantum / Постквантовая криптография**: ML-KEM-768 (NIST FIPS 203)
- 🕸️ **Mesh / Mesh-сеть**: Bluetooth / Wi-Fi Direct / LoRa + TOR/I2P fallback
- 🪪 **DID / Децентрализованная идентичность**: W3C DID, без личных данных
- 📴 **Offline-first / Офлайн-первичность**: работает без интернета
- 🔒 **E2E by default / E2E по умолчанию**: hybrid ML-KEM + X25519

## 🚧 Status / Статус

Early prototype / Ранний прототип.

- [x] ML-KEM-768 key exchange prototype / прототип обмена ключами
- [ ] Hybrid KEM (ML-KEM + X25519) / гибридный KEM
- [ ] P2P transport / P2P-транспорт
- [ ] DID identity / DID-идентичность
- [ ] Mobile UI / мобильный UI

## 🛡️ Threat model (planned) / Модель угроз (в планах)

- Quantum adversary / противник с квантовым компьютером
- Network surveillance / сетевая слежка
- Centralized censorship / централизованная цензура

Honest THREAT_MODEL.md — coming soon / скоро.

## ⚖️ Ethics / Этика

Lantern is a privacy protection tool / Lantern — инструмент защиты приватности.
Responsibility for use lies with the user / ответственность за использование — на пользователе.
White-hat only / только white-hat.

---

**Made with ❤️ for the right to privacy / Сделано с ❤️ для права на приватность**
