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

`Expedition` es un `OperationType`, no una raíz separada.

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

## 11. Seguridad

- Backend valida permisos siempre.
- Frontend solo oculta acciones; no es seguridad.
- Permisos deben soportar módulo, recurso, acción y campo.
- Todo cambio sensible exige auditoría.
- Credenciales externas se almacenan mediante `secretRef` o `configRef`, nunca texto plano.

## 12. Regla final

Si una implementación funciona pero rompe estas directrices, se rechaza.
