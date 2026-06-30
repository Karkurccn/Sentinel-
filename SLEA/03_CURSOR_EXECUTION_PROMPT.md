# SLEA — Cursor / Kiro Execution Prompt

## Rol

Actúa como arquitecto senior y desarrollador full-stack enterprise para Sentinel Logistic Truck.

Tu misión no es rediseñar el negocio. Tu misión es implementar respetando la arquitectura SLEA.

## Directiva central

Implementa Sentinel Logistic Truck como Modular Monolith, multi-tenant, multi-company, API-first, metadata-driven y event-driven interno.

No crear microservicios en esta etapa.

## Reglas no negociables

1. Todo dato operacional debe tener `tenantId` y `companyId`.
2. Todo módulo debe tener Settings, Catalogs, Permissions, Audit, Events y Health.
3. No hardcodear listas de negocio.
4. No guardar binarios en base de datos.
5. No duplicar datos maestros dentro de Operation.
6. No escribir directamente tablas propiedad de otro módulo.
7. No crear flujos paralelos a Operation Core.
8. Toda mutación relevante genera auditoría.
9. Toda acción de negocio importante publica evento.
10. Backend bloquea permisos; frontend solo oculta acciones.

## Módulos aprobados

Implementar en este orden recomendado:

1. Platform Core foundation.
2. Identity Core.
3. Document Core.
4. Customer Core.
5. Fleet Core.
6. Driver Core.
7. Inventory Core.
8. Planning Core.
9. Operation Core.
10. Telematics & IoT Core.
11. Tire Core.
12. Financial Operations Core.
13. Workflow & Notification Core.
14. Analytics & BI Core.
15. Integration Hub.
16. AI & Automation Core.

## Entregable esperado por módulo

Para cada módulo entregar:

- Migraciones.
- Models/entities.
- DTOs.
- Services.
- Controllers/routes.
- Permission guards.
- Settings resolver.
- Catalog resolver.
- Audit logger integration.
- Event publisher integration.
- Health endpoint.
- UI workspace mínimo.
- Tests mínimos.
- Documentación de APIs.

## Arquitectura backend esperada

Estructura sugerida:

```text
src/
  modules/
    identity/
    customer/
    fleet/
    driver/
    inventory/
    document/
    planning/
    operation/
    telematics/
    tire/
    financial-operations/
    workflow-notification/
    analytics/
    integration-hub/
    ai-automation/
    platform/
  shared/
    audit/
    events/
    permissions/
    settings/
    catalogs/
    storage/
    health/
```

## Arquitectura frontend esperada

Cada módulo debe tener:

```text
pages/{module}/
  index
  dashboard
  workspace/:id
  settings
  catalogs
components/{module}/
services/{module}Api
```

## Operation Core

Operation es la entidad raíz operacional.

OperationType incluye:

- EXPEDITION
- TRANSFER
- PICKUP
- DISTRIBUTION
- RETURN
- SERVICE

## Inventario

No implementar reservas formales como flujo principal.

Implementar:

- Direct load.
- Build load selection.
- Optional consolidation.
- StockMovement en cada cambio físico.

## Telematics

Implementar soporte para GPS Gateway externo:

- tenantId
- token
- device mapping
- normalized payload
- start/stop detection
- stop reason request
- deviation detection

## Tire Core

Tire Core es módulo independiente.

Debe soportar:

- Número de fuego.
- RFID.
- Portales.
- TPMS.
- Presión manual.
- Profundidad.
- Km ledger.
- Anomalías.
- Bloqueo de despacho por estado crítico.

## Financial Operations

No reemplaza ERP contable.

Debe manejar:

- Funding.
- Gastos.
- Cuentas por pagar.
- Cuentas por cobrar.
- Pagos a proveedores.
- Evidencias de medio de pago.
- Receptor del pago.
- Flujo de caja simple.
- Forecast.

## Criterio de éxito

Una implementación es aceptada si:

- Respeta SLEA.
- No introduce duplicidad.
- No crea flujos paralelos.
- Es auditable.
- Es configurable.
- Es segura.
- Es testeable.
- Es extensible.

## Forma de trabajo

Antes de codificar cada módulo:

1. Leer `SLEA/00_ARCHITECTURE_DIRECTIVES.md`.
2. Leer `SLEA/01_DELIVERY_REQUIREMENTS.md`.
3. Leer `SLEA/02_MODULE_BLUEPRINTS.md`.
4. Crear plan técnico.
5. Implementar.
6. Validar checklist.
7. Documentar decisiones.

No improvisar arquitectura.
