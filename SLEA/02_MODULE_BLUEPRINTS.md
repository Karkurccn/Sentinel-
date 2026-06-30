# SLEA — Module Blueprints

## 1. Objetivo

Este documento resume los módulos aprobados de Sentinel Logistic Truck, su propósito, límites y entregables esperados. Cursor debe usarlo para bajar cada módulo a implementación concreta.

---

# 2. Security Baseline / Identity Core

## Propósito
Gobierna identidad, autenticación, autorización, perfiles, roles, permisos granulares, módulos por empresa y replicación para holdings.

La seguridad es fundacional. Debe implementarse antes de los módulos operativos.

## Entidades base
- Tenant
- CompanyGroup
- Company
- User
- UserCompanyAccess
- Role
- Profile
- Permission
- ModuleActivation
- ProfileTemplate
- PermissionTemplate
- Session
- RefreshToken
- ApiKey
- MfaFactor
- MfaChallenge
- RecoveryCode
- TrustedDevice
- SecurityAuditLog

## Reglas
- Los usuarios pertenecen al tenant, no se duplican por empresa.
- Un usuario puede tener perfiles distintos por empresa.
- Los módulos se activan por Company.
- Permisos granulares por módulo, recurso, acción y campo.
- MFA / doble factor es obligatorio como capacidad base.
- MFA puede exigirse por tenant, company, perfil, rol, módulo o acción crítica.
- Step-up authentication debe existir para acciones críticas.
- Sesiones, refresh tokens y API keys deben ser revocables.
- Todo acceso y cambio sensible se audita.

---

# 3. Customer Core

## Propósito
Cliente como entidad logística y comercial, no solo RUT.

## Submódulos
- Customers
- Contacts
- Locations
- Operational Rules
- Commercial Rules
- Tariffs
- Tariff History
- Contracts
- Billing History
- Customer 360

## Reglas
- Tarifa se define en Customer.
- Tarifa aplicada se congela en Operation/Finance.
- Cliente puede tener ubicaciones, geocercas, reglas y documentos requeridos.

---

# 4. Fleet Core

## Propósito
Administra tractos, ramplas, disponibilidad, documentos, GPS assignment y asset finance.

## Submódulos
- Trucks
- Trailers
- Fleet Documents
- Availability
- GPS Assignment
- Fleet Groups
- Asset Finance
- Installments

## Reglas
- Fleet no crea operaciones.
- Fleet solo presta recursos.
- GPS Core procesa datos; Fleet solo asocia dispositivo.
- Tire Core controla neumáticos; Fleet solo visualiza posición.

---

# 5. Driver Core

## Propósito
Administra conductores, documentos, licencias, disponibilidad, jornada legal, estados y performance.

## Submódulos
- Drivers
- Driver Documents
- Availability
- Driver Status Log
- Shifts
- Rest Rules
- Assignment History
- Performance
- Wallet Link

## Reglas
- El conductor debe marcar estado operacional/legal.
- Estados: conduciendo, descanso, espera, carga, descarga, fiscalización, panne, combustible, comida, fin jornada.
- GPS puede detectar inconsistencias contra estado declarado.

---

# 6. Inventory Core

## Propósito
Custodia carga física disponible.

## Submódulos
- Warehouses
- Inventory Items
- Stock Lots
- Stock Movements
- Inventory Selection
- Optional Consolidation
- Load Actions
- Valuation

## Reglas
- No usar reserva formal como regla principal.
- Permitir carga directa, selección para armado y consolidación opcional.
- Stock se consume por movimiento LOAD salvo setting contrario.
- Todo movimiento genera StockMovement.

---

# 7. Document Core

## Propósito
Servicio transversal para documentos, evidencias, OCR, IA, firmas, versiones y storage externo.

## Reglas
- No guardar binarios en DB.
- Un documento puede relacionarse con múltiples módulos.
- Usar DocumentRelation.
- OCR y payloads pesados pueden ir a storage externo.

---

# 8. Planning Core

## Propósito
Cotizador y motor de planificación: rutas, costos, escenarios, ETA, peajes, combustible, margen y precio sugerido.

## Reglas
- No limitarse a Route Template.
- Planning calcula escenarios.
- Operation nace desde un planning snapshot aprobado o manual según settings.

---

# 9. Operation Core

## Propósito
Corazón operacional. `Operation` es la entidad raíz técnica.

`Expedición` es el nombre comercial que el cliente usa para la operación. Técnicamente debe mapearse como `OperationType = EXPEDITION` o como label visible configurable, pero no debe crear una raíz paralela.

## Submódulos
- Operations
- Operation Types
- Business Labels
- Segments
- Stops
- Cargo Lines
- Timeline
- Events
- Exceptions
- Snapshots
- Status Machine

## Reglas
- Soporta multi-cliente, multi-camión, multi-rampla, multi-conductor y segmentos.
- No duplica datos maestros.
- Cualquier mutación importante crea evento y auditoría.
- Usa optimistic concurrency.
- En UI puede mostrarse como Expediciones si la Company así lo configura.
- En código, base de datos y contratos debe mantenerse `Operation` como raíz.
- No crear flujo, tabla o servicio `Expedition` que compita con `Operation`.

## OperationType inicial
- EXPEDITION
- TRANSFER
- PICKUP
- DISTRIBUTION
- RETURN
- SERVICE

---

# 10. Telematics & IoT Core

## Propósito
Ingesta y análisis de telemetría: GPS, TPMS, RFID, BLE, CANBus, gateways externos.

## Reglas
- GPS Gateway externo envía tenantId + token.
- No confiar solo en tenantId: validar token.
- Implementar start/stop detection.
- Emitir eventos de movimiento, desvío, geocerca y no señal.

---

# 11. Tire Core

## Propósito
Control independiente del ciclo de vida del neumático.

## Submódulos
- Tire Master
- Número de fuego
- RFID
- Installation History
- Km Ledger
- Manual Inspections
- Tread Depth
- Pressure Measurements
- Portal Reads
- Anomalies
- Retread / Repair / Scrap

## Reglas
- Tire Core es independiente de Fleet y Telematics.
- Telematics alimenta lecturas; Tire interpreta negocio.
- Km se asignan desde OperationSegment cuando corresponde.
- Anomalía crítica puede bloquear despacho.

---

# 12. Financial Operations Core

## Propósito
Finanzas operativas logísticas, no contabilidad ERP.

## Submódulos
- Operation Finance
- Treasury
- Accounts Payable
- Accounts Receivable
- Driver Funding
- Expenses
- Payment Evidence
- Cash Flow Forecast
- Financial Calendar
- Settlements

## Reglas
- Todo gasto debe poder tener evidencia Document Core.
- Pagos a proveedores incluyen medio de pago, evidencia, receptor y aprobador.
- Flujo de caja simple pero ejecutivo.
- Integrable con ERP.

---

# 13. Workflow & Notification Core

## Propósito
Orquesta aprobaciones, tareas, alertas, notificaciones, escalamiento y automatizaciones.

## Canales
- In-app
- Email
- WhatsApp
- SMS
- Webhook

---

# 14. Analytics & BI Core

## Propósito
KPIs, dashboards, scorecards, métricas, forecast, exportación y análisis ejecutivo.

---

# 15. Integration Hub

## Propósito
Todas las integraciones externas viven aquí.

## Integraciones objetivo
- ERP
- Bancos
- SII
- GPS Gateway
- TPMS
- Storage
- WhatsApp
- Email
- OCR
- IA
- MQTT
- N8N

---

# 16. AI & Automation Core

## Propósito
Agentes IA, OCR inteligente, predicciones, asistentes, prompt management y LLM Gateway.

---

# 17. Platform Core

## Propósito
Infraestructura interna: audit, settings, catalogs, feature flags, health, jobs, scheduler, cache, storage, secrets, rate limit, backups, imports/exports.
