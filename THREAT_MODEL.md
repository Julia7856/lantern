# 🛡️ Lantern Threat Model / Модель угроз

**Honest security for privacy-first communication /
Честная безопасность для приватной коммуникации**

> Relative privacy on the network / Относительная приватность в сети.

## Scope / Область действия

Lantern protects against network observation, centralized control, and
post-quantum attacks / Lantern защищает от наблюдения в сети, централизованного
контроля и постквантовых атак.

## Trust boundaries / Границы доверия

| Component / Компонент | Trust / Доверие |
|---|---|
| Local device storage / локальное хранилище | ✅ Trusted / доверенное (user controls / пользователь контролирует) |
| User's private keys / приватные ключи пользователя | ✅ Trusted / доверенные (never leave device / никогда не покидают устройство) |
| Remote peers / удалённые пиры | ❌ Untrusted / недоверенные (verify everything / проверяй всё) |
| Network infrastructure / сетевая инфраструктура | ❌ Untrusted / недоверенная (assume observation / предполагай наблюдение) |
| ML-KEM/X25519 implementations / реализации ML-KEM/X25519 | ✅ Trusted / доверенные (battle-tested libraries / проверенные библиотеки) |

## Threats & mitigations / Угрозы и защита

### 1. Quantum computer attack / атака квантового компьютера
**Attack / Атака:** adversary breaks X25519 with Shor's algorithm /
противник ломает X25519 алгоритмом Шора.
**Mitigation / Защита:** hybrid KEM (X25519 + ML-KEM-768) — if one breaks, the
other holds / гибридный KEM: если один сломается, второй устоит.

### 2. Network observation / наблюдение в сети
**Attack / Атака:** third party with access to network traffic reads it /
третья сторона с доступом к сетевому трафику читает его.
**Mitigation / Защита:** E2E encryption (AES-256-GCM), no plaintext metadata /
E2E-шифрование, без метаданных в открытом виде.

### 3. Harvest now, decrypt later / собрать сейчас, расшифровать потом
**Attack / Атака:** adversary stores encrypted messages, decrypts later when
more powerful computers arrive / противник сохраняет шифртекст, расшифровывает
позже, когда появятся более мощные компьютеры.
**Mitigation / Защита:** ML-KEM-768 provides forward secrecy against future
computational advances / ML-KEM-768 обеспечивает forward secrecy против будущих
вычислительных прорывов.

### 4. Centralized identity risks / риски централизованной идентичности
**Attack / Атака:** a centralized identity provider is a single point of
failure — identifiers can be leaked, revoked, or misused /
централизованный провайдер идентичности — единая точка отказа: идентификаторы
могут утечь, быть отозваны или использованы не по назначению.
**Mitigation / Защита:** W3C DID (self-sovereign identity — the user owns and
controls their identifiers, no central registry needed) /
W3C DID (самосуверенная идентичность — пользователь сам владеет и управляет
своими идентификаторами, центральный реестр не нужен).

### 5. Mesh network isolation / изоляция mesh-сети
**Attack / Атака:** network is partitioned, users become isolated /
сеть разделяется, пользователи становятся изолированными.
**Mitigation / Защита:** hybrid transport (mesh + anonymous overlay networks
fallback) / гибридный транспорт (mesh + fallback на анонимные оверлей-сети).

### 6. Device compromise / компрометация устройства
**Attack / Атака:** malware steals private keys / вредонос крадёт приватные ключи.
**Mitigation / Защита:** keys never leave device, encrypted at rest /
ключи никогда не покидают устройство, зашифрованы в покое.

### 7. Man-in-the-middle during key exchange / MITM при обмене ключами
**Attack / Атака:** an active attacker intercepts the exchange and impersonates
both peers / активный противник перехватывает обмен и выдаёт себя за оба пира.
**Mitigation / Защита:** out-of-band verification (QR / safety numbers), key
pinning on first use (TOFU) / внеполосная верификация (QR / коды безопасности),
закрепление ключа при первом использовании (TOFU).

### 8. Message replay / повтор сообщений
**Attack / Атака:** adversary resends an old ciphertext / противник повторно
отправляет старый шифртекст.
**Mitigation / Защита:** monotonic counters + timestamps, unique nonce per
message / монотонные счётчики + метки времени, уникальный nonce на каждое
сообщение.

### 9. Traffic analysis / анализ трафика
**Attack / Атака:** sizes and timing of messages leak information / размеры и
время сообщений раскрывают информацию.
**Mitigation / Защита (planned / в планах):** padding to fixed blocks, uniform
message format / паддинг до фиксированных блоков, единый формат сообщений.

### 10. Session key compromise / компрометация сессионного ключа
**Attack / Атака:** a session key leaks after use / сессионный ключ утекает после
использования.
**Mitigation / Защита (planned / в планах):** Double Ratchet — a new key per
message, post-compromise security (Signal-style) / Double Ratchet — новый ключ
на каждое сообщение, безопасность после компрометации (как в Signal).

## Planned hardening / Планируемое усиление

- 🔄 Double Ratchet (per-message keys) / ключ на каждое сообщение
- 🔢 Safety numbers / QR verification / коды безопасности / QR-верификация
- 📏 Padding + uniform message size / паддинг + единый размер сообщений
- 👥 MLS for groups (RFC 9420) / MLS для групп
- 🧊 Hardware-backed key storage (Keystore / StrongBox) / хранение ключей в
  аппаратном хранилище
- ⏳ Ephemeral messages (auto-delete) / эфемерные сообщения (автоудаление)

## What we do NOT claim / Что мы НЕ утверждаем

- ❌ Lantern is NOT anonymous against a global passive observer with full
  network visibility — metadata (who talks to whom, when) may leak /
  Lantern НЕ анонимен против глобального пассивного наблюдателя с полным обзором
  сети — метаданные (кто с кем, когда) могут утечь.
- ❌ Lantern does NOT protect against endpoint compromise (if your phone is
  compromised, messages are exposed) / Lantern НЕ защищает от компрометации
  устройства (если телефон скомпрометирован, сообщения раскрыты).
- ❌ Post-quantum cryptography (ML-KEM) is new — theoretical attacks may emerge /
  постквантовая криптография (ML-KEM) новая — могут появиться теоретические атаки.
- ❌ Mesh networks have limited range (~100m for Bluetooth, ~1km for LoRa) /
  mesh-сети имеют ограниченный радиус (~100 м для Bluetooth, ~1 км для LoRa).

## Responsible use / Ответственное использование

Lantern is a privacy protection tool / Lantern — инструмент защиты приватности.
Responsibility for use lies with the user / ответственность за использование — на
пользователе.

For people who value privacy / для людей, которые ценят приватность.
White-hat only / только white-hat.

## Reporting / Сообщение об уязвимостях

GitHub → Security → Report a vulnerability (private) / приватно.
