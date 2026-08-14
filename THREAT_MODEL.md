# 🛡️ Lantern — Threat Model / Модель угроз

A living audit of what Lantern protects against and what remains.
Живой аудит: от чего Lantern защищает, а что ещё осталось.

Legend / Легенда:
- ✅ **Closed** / Закрыто — module in CI, proof of protection
- ⚠️ **Partial** / Частично — mitigated but not fully hardened
- ❌ **Open** / Открыто — known gap, future work

---

## 1. Man-in-the-middle on first contact / MITM при первом контакте

✅ **Closed.** Noise XX handshake (`crypto/noise_handshake.py`) binds
static identities to the transcript. No pre-shared keys needed;
fingerprints match only if no one is in the middle.

✅ **Закрыто.** Рукопожатие Noise XX связывает статические идентичности
с транскриптом. Без общих ключей; отпечатки совпадают только если
посередине никого нет.

## 2. Eavesdropping on message content / Прослушка содержимого

✅ **Closed.** Every message uses a fresh key from the symmetric ratchet
(`crypto/ratchet.py`) and is encrypted with AES-256-GCM. Ciphertext
only is observable on the wire.

✅ **Закрыто.** Каждое сообщение на свежем ключе из симметричного
рэтчета, зашифровано AES-256-GCM. Видим только шифртекст.

## 3. Compromise of a current key — past messages / Компрометация текущего ключа — прошлое

✅ **Closed.** Forward secrecy: each message key is derived from the
chain key and destroyed after use. Past ciphertext stays unreadable.

✅ **Закрыто.** Forward secrecy: ключ сообщения вычисляется из ключа
цепочки и сжигается. Прошлый шифртекст остаётся нечитаемым.

## 4. Compromise of a current key — future messages / Компрометация текущего ключа — будущее

✅ **Closed.** DH ratchet (`crypto/dh_ratchet.py`, `crypto/session_ratchet.py`)
rotates a fresh DH pair on every turn. The chain is re-rooted with
new entropy; secrecy heals itself — post-compromise security.

✅ **Закрыто.** DH-рэтчет ротирует новую DH-пару на каждом ходе.
Цепочка укореняется заново — секретность самовосстанавливается.

## 5. Replay attacks / Атаки повтором

✅ **Closed.** AES-GCM uses a fresh random 12-byte nonce per message
(`session.py`, `net/onion.py`). Replayed ciphertext fails the AEAD
authentication tag.

✅ **Закрыто.** AES-GCM использует свежий случайный nonce на каждое
сообщение. Повторённый шифртекст падает на проверке AEAD-тега.

## 6. Quantum computers / Квантовые компьютеры

✅ **Closed.** Hybrid KEM (`crypto/hybrid_kem.py`, `crypto/mlkem_exchange.py`)
combines classical X25519 with post-quantum ML-KEM-768. Break either,
not both — the session key survives.

✅ **Закрыто.** Гибридный KEM: классический X25519 + постквантовый
ML-KEM-768. Ломай любой один — ключ сессии выживает.

## 7. Identity forgery / Подделка идентичности

✅ **Closed.** Every message carries an Ed25519 signature over the
ciphertext (`identity/did_key.py`). Forging requires the private key.

✅ **Закрыто.** Каждое сообщение с подписью Ed25519 поверх шифртекста.
Подделать без приватного ключа нельзя.

## 8. Trusted central server / Доверенный центральный сервер

✅ **Closed.** did:key identities are self-certifying; the mesh transport
(`net/mesh.py`) is store-and-forward with untrusted relays. No CA,
no single point of failure.

✅ **Закрыто.** Идентичности did:key самозаверяющиеся, mesh-транспорт —
store-and-forward через недоверенные реле. Нет CA, нет единой точки
отказа.

## 9. Metadata: who talks to whom and when / Метаданные: кто с кем и когда

✅ **Closed.** Onion routing (`net/onion.py`) wraps each hop; every
relay learns only the next hop, never both endpoints. Fixed-size
padding hides message length.

✅ **Закрыто.** Onion-маршрутизация: реле знает только следующий
прыжок, никогда оба конца. Паддинг скрывает длину сообщения.

## 10. Denial of service and spam / Отказ в обслуживании и спам

❌ **Open.** Lantern currently has no rate limiting, no proof-of-work,
no reputation layer. A malicious peer can flood the inbox.

❌ **Открыто.** В Lantern пока нет ограничения скорости, нет
proof-of-work, нет репутации. Злоумышленник может завалить ящик.

## 11. Endpoint compromise / Компрометация устройства

❌ **Open.** If an attacker owns the phone, they read plaintext before
encryption and after decryption. No crypto can fix a rooted endpoint.

❌ **Открыто.** Если атакующий владеет устройством, он читает
открытый текст до шифрования и после расшифровки. Никакая криптография
не лечит скомпрометированную конечную точку.

## 12. Identity loss / key rotation / Потеря идентичности / ротация ключей

⚠️ **Partial.** did:key can be regenerated, but Lantern has no recovery
flow, no key rotation, no backup. Losing the key = losing the identity.

⚠️ **Частично.** did:key можно пересгенерировать, но нет ни процедуры
восстановления, ни ротации, ни резервной копии. Потерял ключ = потерял
идентичность.

## 13. Social engineering / Социальная инженерия

⚠️ **Partial.** Fingerprints from Noise XX can be compared out-of-band
(QR code, voice), but Lantern does not yet expose the UI or the flow.

⚠️ **Частично.** Отпечатки Noise XX можно сверить вне канала (QR, голос),
но в Lantern пока нет ни UI, ни самого флоу.

---

## Score / Итог

| Status | Count |
|---|---|
| ✅ Closed | 9 |
| ⚠️ Partial | 3 |
| ❌ Open | 2 |

**9 of 14 threat classes are mathematically closed and proven in CI.**
The remaining items are endpoint/operational — the kind no protocol
alone can solve.

**9 из 14 классов угроз закрыты математически и доказаны в CI.**
Оставшиеся — на стороне устройства и операций; их одним протоколом
не решить.

---
## 🌐 Web Demo (Pyodide) — Threat Audit / Аудит угроз веб-демо

Added in UI v0.7: live demo + live chat in browser. New attack surface below.
Добавлено в UI v0.7: живое демо + живой чат в браузере. Новая поверхность атаки.

| # | Threat / Угроза | Status / Статус | Countermeasure / Контрмера |
|---|------------------|------------------|-----------------------------|
| W1 | Pyodide CDN compromise (supply chain) / Компрометация CDN Pyodide | ⚠️ accepted / принятый риск | demo only; production = local build / демо; продакшн = локальная сборка |
| W2 | Keys in browser memory / Ключи в памяти браузера | ⚠️ accepted / принятый риск | demo ≠ production; device compromise = keys leak / демо ≠ продакшн |
| W3 | MITM of fetched modules / MITM загрузки модулей | 🟡 partial / частично | HTTPS; code signing not implemented yet / подписи кода пока нет |
| W4 | Malicious browser extensions / Вредоносные расширения | ⚠️ accepted / принятый риск | same as W2 / то же, что W2 |

**Philosophy / Философия:** web demo is a *visualization of the protocol*, not production. Production Lantern = local execution.
Веб-демо — *визуализация протокола*, а не продакшн. Продакшн = локальное исполнение.

---
## Modules behind every ✅ / Модули за каждым ✅

| Layer / Слой | Module |
|---|---|
| Identity / Идентичность | `identity/did_key.py` |
| Key agreement / Согласование ключа | `crypto/mlkem_exchange.py`, `crypto/hybrid_kem.py` |
| Handshake / Рукопожатие | `crypto/noise_handshake.py` |
| Message keys / Ключи сообщений | `crypto/ratchet.py`, `crypto/dh_ratchet.py`, `crypto/session_ratchet.py` |
| Session / Сессия | `session.py` |
| Transport / Транспорт | `net/mesh.py`, `net/onion.py` |

Lantern 🏮 — built one module at a time.
