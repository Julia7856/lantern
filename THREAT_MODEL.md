# 🛡️ Lantern Threat Model / Модель угроз

**Honest security for privacy-first communication /
Честная безопасность для приватной коммуникации**

> Privacy is a right, not a feature.
> Приватность — это право, а не функция.

## Scope / Область действия

Lantern protects against network surveillance, centralized control, and
post-quantum attacks / Lantern защищает от сетевой слежки, централизованного
контроля и постквантовых атак.

## Trust boundaries / Границы доверия

| Component / Компонент | Trust / Доверие |
|---|---|
| Local device storage / локальное хранилище | ✅ Trusted / доверенное (user controls / пользователь контролирует) |
| User's private keys / приватные ключи пользователя | ✅ Trusted / доверенные (never leave device / никогда не покидают устройство) |
| Remote peers / удалённые пиры | ❌ Untrusted / недоверенные (verify everything / проверяй всё) |
| Network infrastructure / сетевая инфраструктура | ❌ Untrusted / недоверенная (assume surveillance / предполагай слежку) |
| ML-KEM/X25519 implementations / реализации ML-KEM/X25519 | ✅ Trusted / доверенные (battle-tested libraries / проверенные библиотеки) |

## Threats & mitigations / Угрозы и защита

### 1. Quantum computer attack / атака квантового компьютера
**Attack / Атака:** adversary breaks X25519 with Shor's algorithm /
противник ломает X25519 алгоритмом Шора.
**Mitigation / Защита:** hybrid KEM (X25519 + ML-KEM-768) — if one breaks, the
other holds / гибридный KEM: если один сломается, второй устоит.

### 2. Network surveillance / сетевая слежка
**Attack / Атака:** ISP or state monitors traffic / провайдер или государство
мониторит трафик.
**Mitigation / Защита:** E2E encryption (AES-256-GCM), no plaintext metadata /
E2E-шифрование, без метаданных в открытом виде.

### 3. Harvest now, decrypt later / собрать сейчас, расшифровать потом
**Attack / Атака:** adversary stores encrypted messages, decrypts when quantum
computers arrive / противник сохраняет шифртекст, расшифровывает когда появятся
квантовые компьютеры.
**Mitigation / Защита:** ML-KEM-768 provides forward secrecy against quantum
attacks / ML-KEM-768 обеспечивает forward secrecy против квантовых атак.

### 4. Centralized identity coercion / принуждение к централизованной идентичности
**Attack / Атака:** state requires phone/passport for messaging / государство
требует телефон/паспорт для мессенджера.
**Mitigation / Защита:** W3C DID (decentralized identity, no central authority) /
W3C DID (децентрализованная идентичность, без центрального органа).

### 5. Mesh network isolation / изоляция mesh-сети
**Attack / Атака:** adversary partitions mesh network, isolates users /
противник разделяет mesh-сеть, изолирует пользователей.
**Mitigation / Защита:** hybrid transport (mesh + TOR/I2P fallback) /
гибридный транспорт (mesh + fallback на TOR/I2P).

### 6. Device compromise / компрометация устройства
**Attack / Атака:** malware steals private keys / вредонос крадёт приватные ключи.
**Mitigation / Защита:** keys never leave device, encrypted at rest /
ключи никогда не покидают устройство, зашифрованы в покое.

## What we do NOT claim / Что мы НЕ утверждаем

- ❌ Lantern is NOT anonymous against a global passive adversary with full
  network visibility — metadata (who talks to whom, when) may leak /
  Lantern НЕ анонимен против глобального пассивного противника с полным обзором
  сети — метаданные (кто с кем, когда) могут утечь.
- ❌ Lantern does NOT protect against endpoint compromise (if your phone is
  hacked, messages are exposed) / Lantern НЕ защищает от компрометации
  устройства (если телефон взломан, сообщения раскрыты).
- ❌ Post-quantum cryptography (ML-KEM) is new — theoretical attacks may emerge /
  постквантовая криптография (ML-KEM) новая — могут появиться теоретические атаки.
- ❌ Mesh networks have limited range (~100m for Bluetooth, ~1km for LoRa) /
  mesh-сети имеют ограниченный радиус (~100 м для Bluetooth, ~1 км для LoRa).

## Responsible use / Ответственное использование

Lantern is a privacy protection tool / Lantern — инструмент защиты приватности.
Responsibility for use lies with the user / ответственность за использование — на
пользователе.

White-hat only: journalists, activists, human rights defenders, privacy-conscious
individuals / только white-hat: журналисты, активисты, правозащитники, люди,
ценящие приватность.

## Reporting / Сообщение об уязвимостях

GitHub → Security → Report a vulnerability (private) / приватно.
