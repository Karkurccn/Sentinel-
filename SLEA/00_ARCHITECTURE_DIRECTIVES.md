# SLEA — Architecture Directives

## 1. Objetivo

Este documento define las directrices maestras de arquitectura para Sentinel Logistic Truck. Cursor/Kiro debe implementar siguiendo estas reglas sin reinterpretar el negocio ni crear flujos paralelos.

## 2. Modelo de arquitectura

Sentinel se implementa como **Modular Monolith**:

- Una sola base de datos transaccional.
- Separación lógica por módulos de dominio.
- Servicios internos por módulo.
- APIs contract-first.
- Eventos internos para coordinación.
- Storage externo para archivos.

No implementar microservicios en esta etapa.

## 3. Jerarquía multi-tenant

```text
Tenant
  └── CompanyGroup / Holding
        └── Company
              └── Users / Profiles / Modules / Data
```

Reglas:

- Todo dato operacional debe tener `tenantId` y `companyId`.
- Los módulos se activan por `Company`, no solo por Tenant.
- Un usuario puede tener perfiles distintos por empresa.
- Los perfiles y permisos pueden replicarse entre empresas de un holding.

## 4. Módulos aprobados

1. Identity Core
2. Customer Core
3. Fleet Core
4. Driver Core
5. Inventory Core
6. Document Core
7. Planning Core
8. Operation Core
9. Telematics & IoT Core
10. Tire Core
11. Financial Operations Core
12. Workflow & Notification Core
13. Analytics & BI Core
14. Integration Hub
15. AI & Automation Core
16. Platform Core

## 5. Reglas obligatorias por módulo

Todo módulo debe incluir:

- Data model.
- Service layer.
- API contracts.
- Settings.
- Catalogs.
- Field definitions.
- Permissions.
- Audit trail.
- Events.
- Health check.
- Workspace definition.
- Dashboard/KPIs.
- Cursor acceptance criteria.

## 6. Ownership

Cada módulo es dueño de su dominio. Ningún módulo debe escribir directamente datos de otro módulo.

Ejemplos:

- Driver Core es dueño de conductores.
- Fleet Core es dueño de tractos y ramplas.
- Tire Core es dueño del ciclo de vida del neumático.
- Document Core es dueño de documentos y evidencias.
- Operation Core orquesta, pero no duplica datos maestros.

## 7. Operation Core como núcleo operacional

La entidad raíz operacional es `Operation`.

`Expedition` / `Expedición` **no es una entidad raíz separada**. Es un `OperationType` y también un **nombre comercial/operativo** que algunos clientes usan para referirse a cualquier operación logística.

Regla de naming:

- En base de datos y dominio técnico, usar `Operation`.
- En UI se puede mostrar `Expedición` cuando el cliente llame así a sus operaciones.
- El label visible debe ser configurable por Company mediante settings/catálogos.
- No crear tablas, servicios o flujos paralelos llamados `Expedition` que compitan con `Operation`.
- Si aparece legacy `Expedition`, debe migrarse o mapearse hacia `Operation`.

Operation debe soportar:

- Multi-cliente.
- Multi-camión.
- Multi-rampla.
- Multi-conductor.
- Segmentos.
- Carga directa.
- Carga parcial.
- Consolidación opcional.
- Timeline.
- Eventos.
- Excepciones.
- Snapshots.
- Cierre operativo y económico.

## 8. Metadata Driven

El código define capacidades. La metadata define comportamiento.

Debe ser configurable:

- Campos.
- Catálogos.
- Estados.
- Settings.
- Workflows.
- Validaciones.
- Dashboards.
- KPIs.
- Permisos.
- Feature flags.
- Labels de negocio, incluyendo que `Operation` se muestre como `Expedición` cuando el cliente lo requiera.

## 9. Document Core transversal

Todo archivo o evidencia debe vivir fuera de la base de datos.

La base guarda:

- Metadata.
- Relaciones.
- Permisos.
- OCR resumido.
- Auditoría.
- Rutas de storage.

Document Core sirve a todos los módulos: facturas, OC, guías, peajes, boletas, licencias, revisiones técnicas, evidencias, fotos, videos, audios, POD, contratos y OCR.

## 10. Integration Hub

Toda integración externa debe pasar por Integration Hub:

- ERP.
- GPS Gateway.
- TPMS.
- Bancos.
- SII.
- WhatsApp.
- Email.
- Storage.
- OCR.
- IA.
- MQTT.
- N8N.

Los módulos de negocio no deben integrar directamente proveedores externos.

## 11. Seguridad como base esencial

La seguridad no es una fase posterior ni un módulo opcional. Es **punto base obligatorio** de la plataforma.

Reglas mínimas:

- Backend valida permisos siempre.
- Frontend solo oculta acciones; no es seguridad.
- Permisos deben soportar módulo, recurso, acción y campo.
- Todo cambio sensible exige auditoría.
- Credenciales externas se almacenan mediante `secretRef` o `configRef`, nunca texto plano.
- Implementar doble factor de autenticación / MFA desde la base.
- MFA debe ser configurable por Tenant y Company.
- MFA debe poder ser obligatorio por perfil, rol, módulo o acción crítica.
- Acciones críticas deben poder exigir step-up authentication aunque el usuario ya esté logueado.
- Sesiones, refresh tokens y API keys deben ser revocables.
- Toda autenticación fallida debe auditarse.
- Todo acceso administrativo debe auditarse.

MFA mínimo esperado:

- TOTP Authenticator App.
- Email OTP como fallback controlado.
- Recovery codes.
- Política para forzar enrolamiento.
- Registro de dispositivo confiable configurable.

Acciones críticas que deben soportar step-up MFA:

- Cambiar permisos.
- Activar/desactivar módulos.
- Ejecutar pagos.
- Aprobar liquidaciones.
- Cerrar operación económicamente.
- Ver o exportar información sensible.
- Impersonation.
- Rotar tokens o secrets.

## 12. Regla final

Si una implementación funciona pero rompe estas directrices, se rechaza.
