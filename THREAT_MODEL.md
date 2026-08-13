# 🛡️ Lantern Threat Model / Модель угроз

**Honest security for privacy-first communication /
Честная безопасность для приватной коммуникации**

> Privacy is a right, not a feature.
> Приватность — это право, а не функция.

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

## What we do NOT claim / Что мы НЕ утверждаем

- ❌ Lantern is NOT anonymous against a global passive observer with full
  network visibility — metadata (who talks to
