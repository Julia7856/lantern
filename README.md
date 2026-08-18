# 🏮 Lantern

**Post-quantum private P2P communicator / Приватный P2P-коммуникатор с постквантовой криптографией и mesh-сетью**

> Relative privacy on the network / Относительная приватность в сети.

## 🎯 What is this? / Что это?

Lantern — децентрализованный коммуникатор: без телефона, без паспорта, без центрального сервера / a decentralized communicator: no phone, no passport, no central server.

- 🧬 **Post-quantum / Постквантовая криптография**: ML-KEM-768 (NIST FIPS 203)
- 🔒 **E2E by default / E2E по умолчанию**: hybrid ML-KEM + X25519 → AES-256-GCM
- ⏳ **HNDL-resistant / Устойчив к HNDL**: гибридный KEM защищает даже трафик, записанный сегодня / hybrid KEM protects even traffic recorded today
- 🕸️ **Mesh / Mesh-сеть**: Bluetooth / Wi-Fi Direct / LoRa + anonymous overlay fallback
- 🪪 **DID / Децентрализованная идентичность**: W3C did:key, без личных данных
- 📴 **Offline-first / Офлайн-первичность**: работает без интернета

## 📁 Structure / Структура

- `crypto/mlkem_exchange.py` — ML-KEM-768 key exchange / обмен ключами
- `crypto/hybrid_kem.py` — hybrid KEM (X25519 + ML-KEM) / гибридный KEM
- `crypto/secure_message.py` — AES-256-GCM encryption / шифрование сообщений
- `crypto/ratchet.py` — symmetric ratchet, per-message keys / симметричный рэтчет
- `crypto/dh_ratchet.py` — DH ratchet, healing / DH-рэтчет, лечение
- `crypto/session_ratchet.py` — Double Ratchet session / Double Ratchet
- `crypto/noise_handshake.py` — Noise XX handshake / рукопожатие Noise XX
- `identity/did_key.py` — did:key identity (Ed25519) / DID-идентичность
- `net/mesh.py` — store-and-forward mesh, untrusted relays / P2P mesh-транспорт
- `net/onion.py` — onion routing, metadata protection / onion-маршрутизация
- `session.py` — E2E session v3 demo / демо сессии v3
- `docs/index.html` — web demo: Pyodide + live chat / веб-демо + живой чат
- `docs/manifest.webmanifest` — PWA manifest: install as app / манифест PWA
- `docs/icon.svg` — app icon 🏮 / иконка приложения
- `THREAT_MODEL.md` — honest threat model / честная модель угроз

## 🚧 Status / Статус

Early prototype / Ранний прототип.

- [x] ML-KEM-768 key exchange prototype / прототип обмена ключами
- [x] Hybrid KEM (ML-KEM + X25519) / гибридный KEM
- [x] AES-256-GCM message encryption / шифрование сообщений
- [x] DID identity (did:key, Ed25519) / DID-идентичность
- [x] THREAT_MODEL.md (14 threats + web audit W1–W4 / 14 угроз + веб-аудит)
- [x] End-to-end session demo / сквозная сессия (v3)
- [x] Double Ratchet (per-message keys + healing / ключ на сообщение + лечение)
- [x] P2P transport prototype / прототип P2P-транспорта (mesh + onion)
- [x] Web UI + live chat in browser / веб-UI + живой чат (Pyodide)
- [x] Mobile UI (PWA) — app on home screen / приложение на домашнем экране
- [x] Real network P2P via MQTT relay / настоящий сетевой P2P через MQTT-реле

## 🛡️ Threat model / Модель угроз

See / см. [THREAT_MODEL.md](THREAT_MODEL.md)

## 🌐 Web Demo / Веб-демо

**Live / Вживую:** https://julia7856.github.io/lantern/

Demo runs the real stack in your browser (Pyodide): hybrid root ML-KEM + X25519, Double Ratchet, Ed25519 signatures, live chat. Installable as PWA / ставится как PWA.
Демо гоняет настоящий стек в браузере (Pyodide): гибридный корень, Double Ratchet, подписи, живой чат. Устанавливается как приложение.

### 🌐 Network Room / Сетевая комната (v0.12)

Click **🌐 Комната** → enter 4-letter code (e.g. `ALBA`) → connect. Open the same room from another browser or device → messages flow through the public MQTT relay, but only ciphertext is visible to the relay. Keys rotate locally in Pyodide / жми **🌐 Комната** → введи 4-буквенный код (напр. `ALBA`) → подключись. Открой ту же комнату с другого браузера или устройства → сообщения идут через публичное MQTT-реле, но реле видит только шифртекст. Ключи крутятся локально в Pyodide.

**Test / тест:** Chrome + Samsung Internet on the same phone, same room code / Chrome + Samsung Internet на одном телефоне, один и тот же код.

**Honest limits / честные ограничения:**
- Fixed nonce per session (`\x00` × 12) — production needs unique nonce per message / фиксированный nonce на сессию — в продакшене нужен уникальный на сообщение
- Ratchet state is not synced between devices on connect / состояние рэтчета не синхронизируется при подключении
- No persistence — page reload resets the session / нет persistence — перезагрузка страницы сбрасывает сессию

These limits match THREAT_MODEL.md W1–W4: demo shows architecture, not production readiness / эти ограничения соответствуют W1–W4 THREAT_MODEL.md: демо показывает архитектуру, а не готовность к продакшену.

⚠️ **Demo, not production / Демо, а не продакшн.** Keys live in browser memory / ключи живут в памяти браузера. See THREAT_MODEL.md (W1–W4).

## ⚖️ Ethics / Этика

Lantern is a privacy protection tool / Lantern — инструмент защиты приватности.
Responsibility for use lies with the user / ответственность за использование — на пользователе.

For people who value privacy / для людей, которые ценят приватность.
White-hat only / только white-hat.

## License / Лицензия

© 2026 Julia7856. Non-commercial use is free. Commercial use requires permission — open an Issue.
© 2026 Julia7856. Некоммерческое использование бесплатно. Коммерческое использование — по согласованию (открой Issue).

## Author / Автор

Julia7856 — author of **Lantern** (post-quantum P2P communicator), **Grail** (local data guardian) and **CryptoAudit** (static crypto auditor with PQC checks).
Автор **Lantern** (постквантовый P2P-коммуникатор), **Grail** (локальный защитник данных) и **CryptoAudit** (статический аудитор крипто-кода с PQC-проверками).

---

**Made with ❤️ for people who value privacy / Сделано с ❤️ для людей, которые ценят приватность**
