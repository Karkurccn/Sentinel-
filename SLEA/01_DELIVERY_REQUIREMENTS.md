# SLEA — Delivery Requirements

## 1. Objetivo

Este documento define qué debe entregar Cursor/Kiro por cada módulo implementado. No basta con crear pantallas o tablas. Cada módulo debe salir con una entrega completa, testeable y alineada a la arquitectura.

## 2. Entregables obligatorios por módulo

Para cada módulo, Cursor/Kiro debe entregar:

### 2.1 Backend

- Models / Entities.
- DTOs.
- Services.
- Controllers / Routes.
- Repositories si aplica.
- Validaciones.
- Settings resolver.
- Catalog resolver.
- Permission guards.
- Audit logger.
- Event publisher.
- Health endpoint.
- Tests mínimos.

### 2.2 Base de datos

- Migraciones.
- Índices.
- Foreign keys cuando aplique.
- Campos base obligatorios:
  - `id`
  - `tenantId`
  - `companyId`
  - `status`
  - `version`
  - `createdAt`
  - `updatedAt`
  - `createdByUserId`
  - `updatedByUserId`

### 2.3 API

Cada módulo debe exponer APIs consistentes:

```http
GET /api/{module}
POST /api/{module}
GET /api/{module}/{id}
PATCH /api/{module}/{id}
GET /api/{module}/{id}/audit
GET /api/{module}/{id}/events
GET /api/{module}/settings/effective
GET /api/{module}/health
```

Cuando aplique, agregar endpoints de acciones de dominio, no formularios de pantalla.

### 2.4 Frontend

Cada módulo debe tener:

- Dashboard.
- Listado.
- CRUD.
- Workspace de detalle.
- Timeline.
- Documentos.
- Auditoría.
- Settings.
- Catálogos.
- KPIs.

### 2.5 Seguridad

- Permission guards backend.
- Field-level permissions cuando aplique.
- Scope por tenant/company.
- Data scopes: own, assigned, company, warehouse, customer, route, fleet group.

### 2.6 Auditoría

Toda mutación importante debe registrar:

- actor.
- before.
- after.
- reason.
- moduleKey.
- entityType.
- entityId.
- tenantId.
- companyId.
- timestamp.

### 2.7 Eventos

Cada módulo debe publicar eventos de negocio.

Formato estándar:

```json
{
  "eventId": "uuid",
  "eventType": "DomainEvent",
  "tenantId": "tenant_001",
  "companyId": "company_001",
  "moduleKey": "module_core",
  "entityType": "Entity",
  "entityId": "uuid",
  "occurredAt": "ISO_DATE",
  "payload": {}
}
```

### 2.8 Settings, catálogos y campos dinámicos

Cada módulo debe soportar:

- `ModuleSetting`
- `ModuleCatalog`
- `ModuleCatalogOption`
- `ModuleFieldDefinition`
- `UnitOfMeasure` cuando aplique

No hardcodear listas editables.

## 3. Criterios de aceptación

Un módulo se considera terminado cuando:

- Compila.
- Tiene migraciones.
- Tiene APIs.
- Tiene UI mínima funcional.
- Respeta permisos.
- Registra auditoría.
- Publica eventos.
- Respeta tenant/company.
- Tiene settings y catálogos.
- Tiene tests mínimos.
- Está documentado.

## 4. Prohibiciones

No hacer:

- Crear lógica de negocio en frontend.
- Acceder directo a tablas de otro módulo.
- Guardar archivos pesados en DB.
- Hardcodear catálogos de negocio.
- Crear flujos paralelos al Operation Core.
- Duplicar clientes, conductores, vehículos o documentos dentro de Operation.
- Crear microservicios antes de validar el monolito modular.
