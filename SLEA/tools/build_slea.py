#!/usr/bin/env python3
"""
Sentinel Logistic Truck Enterprise Architecture generator.

This script generates the SLEA documentation repository structure in Markdown.
Run from repository root:

    python SLEA/tools/build_slea.py

It is intentionally self-contained: no external dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from textwrap import dedent
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[2]
SLEA = ROOT / "SLEA"


@dataclass
class ModuleSpec:
    number: int
    key: str
    name: str
    purpose: str
    responsibilities: List[str]
    entities: Dict[str, List[str]] = field(default_factory=dict)
    settings: List[str] = field(default_factory=list)
    events: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)


GLOBAL_PRINCIPLES = [
    "Modular Monolith",
    "Domain Driven Design",
    "API First",
    "Metadata Driven",
    "Event Driven interno",
    "Multi-Tenant",
    "Multi-Company",
    "Storage desacoplado",
    "Auditoría total",
    "Configuración antes que código",
]

MODULES: List[ModuleSpec] = [
    ModuleSpec(
        1,
        "identity_core",
        "Identity Core",
        "Gobierna identidad, autenticación, autorización, perfiles, roles, permisos y activación de módulos por empresa.",
        ["Usuarios", "Roles", "Perfiles", "Permisos granulares", "Multi-tenant", "Multi-company", "MFA", "API Keys", "Sesiones", "Replicación holding"],
        {
            "Tenant": ["id", "code", "name", "status", "createdAt", "updatedAt"],
            "Company": ["id", "tenantId", "companyGroupId", "legalName", "tradeName", "taxId", "country", "timezone", "currency", "status"],
            "User": ["id", "tenantId", "username", "firstName", "lastName", "email", "phone", "passwordHash", "mfaEnabled", "status", "lastLoginAt"],
            "Profile": ["id", "tenantId", "companyId", "code", "name", "description", "sourceTemplateId", "syncMode", "status"],
            "Permission": ["id", "tenantId", "companyId", "permissionKey", "moduleKey", "resource", "action", "field", "status"],
            "UserCompanyAccess": ["id", "tenantId", "userId", "companyId", "profileId", "dataScope", "status"],
        },
        ["identity.mfa.required", "identity.password.minLength", "identity.session.timeoutMinutes", "identity.profiles.allowReplication", "identity.modules.companyActivation"],
        ["UserCreated", "UserUpdated", "LoginSucceeded", "LoginFailed", "PermissionChanged", "ProfileReplicated", "ModuleActivated"],
        ["identity.users.create", "identity.users.update", "identity.permissions.assign", "identity.modules.activate", "identity.impersonation.start"],
    ),
    ModuleSpec(
        2,
        "customer_core",
        "Customer Core",
        "Administra clientes como entidades logísticas, incluyendo ubicaciones, contactos, reglas, tarifas, contratos e historial comercial.",
        ["Clientes", "Contactos", "Ubicaciones", "Reglas operativas", "Reglas comerciales", "Tarifas", "Historial tarifario", "Contratos", "Historial de cobranza"],
        {
            "Customer": ["id", "tenantId", "companyId", "rut", "businessName", "tradeName", "customerType", "industry", "status", "paymentTermsDays", "creditLimit"],
            "CustomerLocation": ["id", "tenantId", "companyId", "customerId", "name", "locationType", "address", "lat", "lng", "geoFenceRadiusMeters", "timeWindowStart", "timeWindowEnd"],
            "CustomerTariff": ["id", "tenantId", "companyId", "customerId", "rateType", "routeSnapshotId", "baseAmount", "currency", "validFrom", "validTo", "status"],
            "CustomerTariffHistory": ["id", "tenantId", "companyId", "customerId", "tariffId", "previousValue", "newValue", "changedByUserId", "changeReason", "effectiveFrom"],
        },
        ["customers.requireRut", "customers.allowDuplicateRut", "customers.enableTariffs", "tariffs.requireApprovalOnChange", "billing.blockDispatchIfOverdue"],
        ["CustomerCreated", "CustomerBlocked", "TariffApproved", "ContractExpired", "CustomerLocationUpdated"],
        ["customers.view", "customers.create", "customers.creditLimit.edit", "customers.tariffs.approve", "customers.contracts.upload"],
    ),
    ModuleSpec(
        3,
        "fleet_core",
        "Fleet Core",
        "Administra tractos, ramplas, documentos, disponibilidad, GPS asociado, financiamiento de activos y vida administrativa de flota.",
        ["Tractos", "Ramplas", "Documentos", "Disponibilidad", "GPS assignment", "Asset Finance", "Cuotas", "Depreciación"],
        {
            "Truck": ["id", "tenantId", "companyId", "plate", "internalCode", "brand", "model", "year", "vin", "fuelType", "status", "odometerKm", "assetFinanceId"],
            "Trailer": ["id", "tenantId", "companyId", "plate", "internalCode", "type", "capacityKg", "capacityM3", "axles", "tireCount", "status"],
            "AssetFinance": ["id", "tenantId", "companyId", "assetType", "assetId", "acquisitionType", "purchaseDate", "purchasePrice", "financedAmount", "remainingBalance", "status"],
            "AssetFinanceInstallment": ["id", "tenantId", "companyId", "assetFinanceId", "installmentNumber", "dueDate", "amount", "paidAmount", "status"],
        },
        ["fleet.requireGpsForDispatch", "fleet.blockExpiredDocuments", "fleet.allowThirdPartyFleet", "fleetFinance.enableAssetFinance", "fleetFinance.blockAssetIfFinanceDefault"],
        ["TruckCreated", "TruckBlocked", "TrailerAssigned", "FleetDocumentExpired", "AssetInstallmentOverdue"],
        ["fleet.truck.create", "fleet.truck.block", "fleet.documents.upload", "fleet.finance.view", "fleet.finance.edit"],
    ),
    ModuleSpec(
        4,
        "driver_core",
        "Driver Core",
        "Administra conductores, licencias, documentos, disponibilidad, estados legales, jornada, descanso, desempeño y wallet link.",
        ["Conductores", "Licencias", "Documentos", "Disponibilidad", "Jornada legal", "Estados", "Descansos", "Performance", "Wallet link"],
        {
            "Driver": ["id", "tenantId", "companyId", "rut", "firstName", "lastName", "phone", "licenseType", "licenseExpiration", "status", "currentTruckId", "currentOperationId"],
            "DriverStatusLog": ["id", "tenantId", "companyId", "driverId", "operationId", "segmentId", "status", "startedAt", "endedAt", "durationMinutes", "source"],
            "DriverShift": ["id", "tenantId", "companyId", "driverId", "operationId", "segmentId", "drivingMinutes", "restMinutes", "workMinutes", "status"],
        },
        ["driver.requireValidLicenseForDispatch", "driver.maxContinuousDrivingHours", "driver.requiredRestHours", "driver.requireStatusBeforeDriving"],
        ["DriverCreated", "DriverAssigned", "DriverStatusChanged", "DriverRestViolationDetected", "DriverDocumentExpired"],
        ["drivers.create", "drivers.license.edit", "drivers.status.override", "drivers.documents.upload", "drivers.performance.view"],
    ),
    ModuleSpec(
        5,
        "inventory_core",
        "Inventory Core",
        "Custodia inventario físico disponible, bodegas, movimientos, selección de carga, consolidación opcional y trazabilidad documental.",
        ["Bodegas", "Inventario", "Movimientos", "Selección", "Carga directa", "Consolidación opcional", "Lotes", "Valorización"],
        {
            "Warehouse": ["id", "tenantId", "companyId", "name", "code", "type", "address", "lat", "lng", "status"],
            "InventoryItem": ["id", "tenantId", "companyId", "warehouseId", "customerId", "sku", "description", "unit", "quantityTotal", "quantityLoaded", "quantityAvailable", "originDocumentId", "status"],
            "InventorySelection": ["id", "tenantId", "companyId", "operationId", "warehouseId", "selectionMode", "status", "selectedByUserId"],
            "StockMovement": ["id", "tenantId", "companyId", "inventoryItemId", "warehouseId", "movementType", "quantity", "operationId", "segmentId", "documentId", "reason"],
        },
        ["inventory.allowNegativeStock", "inventory.requireOriginDocument", "inventory.allowDirectLoad", "inventory.enablePreConsolidation", "inventory.consumeOnLoadOnly"],
        ["InventoryReceived", "InventorySelected", "InventoryLoaded", "InventoryAdjusted", "InventoryDelivered"],
        ["inventory.view", "inventory.adjust", "inventory.load.override", "inventory.warehouse.block", "inventory.valuation.view"],
    ),
    ModuleSpec(
        6,
        "document_core",
        "Document Core",
        "Servicio transversal para documentos, evidencias, OCR, IA, firmas, versiones y storage externo.",
        ["Documentos", "Archivos", "Storage", "OCR", "IA", "Versionado", "Relaciones", "Firmas", "Evidencias"],
        {
            "Document": ["id", "tenantId", "companyId", "documentTypeId", "title", "ownerModule", "ownerEntity", "ownerEntityId", "status", "uploadedByUserId"],
            "DocumentFile": ["id", "tenantId", "companyId", "documentId", "storageProvider", "bucketName", "storagePath", "mimeType", "fileSize", "checksum"],
            "DocumentRelation": ["id", "tenantId", "companyId", "documentId", "moduleKey", "entityType", "entityId", "relationType"],
            "DocumentOcrResult": ["id", "tenantId", "companyId", "documentId", "provider", "status", "confidence", "extractedJson", "validatedByUserId"],
        },
        ["documents.enableOCR", "documents.enableVersioning", "documents.defaultStorage", "documents.requireVirusScan", "documents.defaultRetentionYears"],
        ["DocumentUploaded", "DocumentClassified", "DocumentOcrCompleted", "DocumentSigned", "DocumentExpired"],
        ["documents.upload", "documents.download", "documents.ocr.validate", "documents.share", "documents.delete"],
    ),
    ModuleSpec(
        7,
        "planning_core",
        "Planning Core",
        "Cotiza, simula y planifica rutas, costos, escenarios, ETA, peajes, combustible, margen y precio sugerido.",
        ["Route Calculator", "Cost Engine", "Scenario Simulator", "ETA", "Tolls", "GeoCorridor", "Pricing", "Planning Snapshot"],
        {
            "PlanningScenario": ["id", "tenantId", "companyId", "customerId", "originLocationId", "destinationLocationId", "truckId", "trailerId", "plannedKm", "estimatedHours", "status"],
            "PlanningCostLine": ["id", "tenantId", "companyId", "scenarioId", "costType", "amount", "currency", "calculationBasis"],
            "PlanningSnapshot": ["id", "tenantId", "companyId", "scenarioId", "snapshotJson", "plannedCost", "suggestedPrice", "margin", "createdAt"],
        },
        ["planning.defaultMapProvider", "planning.autoCalculateTolls", "planning.autoCalculateFuel", "planning.targetMarginPercent", "planning.requireApprovedScenario"],
        ["ScenarioCalculated", "ScenarioApproved", "PlanningSnapshotCreated", "PriceSuggested"],
        ["planning.calculate", "planning.approve", "planning.pricing.override", "planning.costVariables.edit"],
    ),
    ModuleSpec(
        8,
        "operation_core",
        "Operation Core",
        "Corazón operacional. Orquesta operaciones logísticas, expediciones, segmentos, carga, stops, eventos, estados y snapshots.",
        ["Operations", "Operation Types", "Segments", "Stops", "Cargo", "Timeline", "Events", "Exceptions", "Snapshots", "Status Machine"],
        {
            "Operation": ["id", "tenantId", "companyId", "code", "operationType", "status", "customerIds", "planningSnapshotId", "originChannel", "version"],
            "OperationSegment": ["id", "tenantId", "companyId", "operationId", "segmentNumber", "truckId", "trailerId", "driverId", "plannedKm", "actualKm", "status"],
            "OperationCargoLine": ["id", "tenantId", "companyId", "operationId", "inventoryItemId", "customerId", "quantityPlanned", "quantityLoaded", "quantityDelivered", "loadMode", "status"],
            "OperationStop": ["id", "tenantId", "companyId", "operationId", "sequence", "stopType", "customerId", "locationId", "plannedArrivalAt", "actualArrivalAt", "status"],
        },
        ["operation.allowMultiCustomer", "operation.allowSegments", "operation.requireInventoryReference", "operation.requireDriverStatusTracking", "operation.enableOptimisticConcurrency"],
        ["OperationCreated", "OperationDispatched", "OperationStatusChanged", "OperationSegmentClosed", "OperationClosed"],
        ["operation.create", "operation.dispatch", "operation.close", "operation.override", "operation.status.change"],
    ),
    ModuleSpec(
        9,
        "telematics_iot_core",
        "Telematics & IoT Core",
        "Ingiere, normaliza y analiza telemetría GPS, TPMS, RFID, CANBus, BLE, gateways IoT y eventos de movimiento.",
        ["GPS Gateway", "TPMS Gateway", "Device Registry", "Tracks", "Points", "Start/Stop", "Geofences", "Route Compliance", "ETA"],
        {
            "TelemetryDevice": ["id", "tenantId", "companyId", "deviceType", "manufacturer", "model", "serialNumber", "gatewayId", "status"],
            "GpsGateway": ["id", "tenantId", "companyId", "name", "baseUrl", "tokenRef", "status", "lastSyncAt"],
            "GpsPoint": ["id", "tenantId", "companyId", "gpsTrackId", "deviceId", "operationId", "segmentId", "lat", "lng", "speed", "ignition", "timestamp"],
            "MovementEvent": ["id", "tenantId", "companyId", "operationId", "segmentId", "deviceId", "eventType", "lat", "lng", "detectedAt", "durationSeconds"],
        },
        ["gps.gatewayMode", "gps.requireTenantToken", "gps.startSpeedThresholdKmh", "gps.stopMinDurationMinutes", "gps.enableGeofenceEvents"],
        ["GpsPointReceived", "StartDetected", "StopDetected", "DeviationDetected", "NoSignalDetected"],
        ["telematics.devices.create", "telematics.gateway.configure", "telematics.raw.view", "telematics.override"],
    ),
    ModuleSpec(
        10,
        "tire_core",
        "Tire Core",
        "Administra neumáticos como activos trazables: número de fuego, RFID, mediciones, presión, profundidad, kilómetros, anomalías y ciclo de vida.",
        ["Tire Master", "Fire Number", "RFID", "Inventory", "Installation", "Km Ledger", "Inspections", "Tread", "Pressure", "Anomalies", "Lifecycle"],
        {
            "Tire": ["id", "tenantId", "companyId", "fireNumber", "rfidTagId", "brand", "model", "size", "purchaseDate", "currentTreadDepthMm", "currentPressurePsi", "currentKm", "status"],
            "TireInstallation": ["id", "tenantId", "companyId", "tireId", "assetType", "assetId", "positionCode", "installedAt", "installedKm", "removedAt", "removedKm"],
            "TireKmLedger": ["id", "tenantId", "companyId", "tireId", "operationId", "segmentId", "kmSource", "kmAdded", "totalKmAfter"],
            "TireAnomaly": ["id", "tenantId", "companyId", "tireId", "anomalyType", "severity", "detectedAt", "resolvedAt", "status"],
        },
        ["tires.requireFireNumberUnique", "tires.enableRfidTracking", "tires.lowPressureThresholdPsi", "tires.minTreadDepthCriticalMm", "tires.blockDispatchOnCriticalTire"],
        ["TireCreated", "TireInstalled", "TireMeasured", "TireAnomalyDetected", "TireScrapped"],
        ["tires.create", "tires.install", "tires.measure.edit", "tires.anomaly.resolve", "tires.fireNumber.edit"],
    ),
    ModuleSpec(
        11,
        "financial_operations_core",
        "Financial Operations Core",
        "Administra la operación financiera logística: funding, gastos, pagos, cobros, cuentas por pagar/cobrar, tesorería, caja y flujo proyectado.",
        ["Operation Finance", "Treasury", "Accounts Payable", "Accounts Receivable", "Funding", "Expenses", "Settlement", "Cash Flow", "Financial Calendar"],
        {
            "OperationCharge": ["id", "tenantId", "companyId", "operationId", "customerId", "tariffId", "tariffSnapshotJson", "plannedAmount", "actualAmount", "status"],
            "DriverFunding": ["id", "tenantId", "companyId", "operationId", "driverId", "segmentId", "type", "amount", "status"],
            "Expense": ["id", "tenantId", "companyId", "operationId", "segmentId", "driverId", "category", "amount", "documentId", "status"],
            "PaymentOrder": ["id", "tenantId", "companyId", "supplierId", "amount", "paymentMethod", "receiverName", "documentId", "status"],
        },
        ["finance.requireExpenseDocument", "finance.requirePaymentEvidence", "finance.enableCashFlowForecast", "finance.blockCloseWithPendingExpenses"],
        ["ExpenseSubmitted", "ExpenseApproved", "PaymentOrderCreated", "InvoiceIssued", "OperationSettlementClosed"],
        ["finance.expense.approve", "finance.payment.execute", "finance.settlement.close", "finance.cashflow.view"],
    ),
    ModuleSpec(
        12,
        "workflow_notification_core",
        "Workflow & Notification Core",
        "Orquesta flujos, aprobaciones, tareas, alertas, notificaciones, escalamiento y automatizaciones internas.",
        ["Workflow Definitions", "Workflow Instances", "Approvals", "Tasks", "Alerts", "Notifications", "Escalations", "Templates", "Channels"],
        {
            "WorkflowDefinition": ["id", "tenantId", "companyId", "moduleKey", "name", "triggerEvent", "version", "status"],
            "WorkflowStep": ["id", "workflowDefinitionId", "sequence", "stepType", "assignedRoleId", "conditionJson", "actionJson"],
            "ApprovalRequest": ["id", "tenantId", "companyId", "moduleKey", "entityType", "entityId", "requestedByUserId", "assignedToUserId", "status"],
            "Notification": ["id", "tenantId", "companyId", "userId", "channel", "title", "message", "templateId", "status"],
        },
        ["workflow.enableApprovalFlows", "workflow.enableTasks", "notifications.enableWhatsapp", "notifications.retryFailedNotifications"],
        ["WorkflowStarted", "ApprovalRequested", "ApprovalApproved", "NotificationSent", "AlertEscalated"],
        ["workflow.edit", "workflow.approve", "alerts.dismiss", "notifications.configure"],
    ),
]


def slug(text: str) -> str:
    return text.lower().replace(" & ", "_").replace(" ", "_").replace("/", "_").replace("-", "_")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def md_list(items: List[str]) -> str:
    return "\n".join(f"- {x}" for x in items)


def entity_table(fields: List[str]) -> str:
    rows = ["| Campo | Descripción |", "|---|---|"]
    for f in fields:
        rows.append(f"| `{f}` | Campo definido por el dominio. |")
    return "\n".join(rows)


def module_overview(m: ModuleSpec) -> str:
    return f"""
    # {m.name} — Overview

    ## Objetivo

    {m.purpose}

    ## Responsabilidades

    {md_list(m.responsibilities)}

    ## Principios

    - Multi-Tenant y Multi-Company.
    - API First.
    - Metadata Driven.
    - Auditoría obligatoria.
    - Settings y Catálogos por empresa.
    - No invade ownership de otros módulos.

    ## Límites del Dominio

    Este módulo administra únicamente su propio dominio. Cuando necesita información externa debe utilizar contratos internos o eventos publicados por otros módulos.
    """


def module_data_model(m: ModuleSpec) -> str:
    parts = [f"# {m.name} — Modelo de Datos\n"]
    for entity, fields in m.entities.items():
        parts.append(f"## {entity}\n\n{entity_table(fields)}\n")
    return "\n".join(parts)


def module_business_rules(m: ModuleSpec) -> str:
    return f"""
    # {m.name} — Reglas de Negocio

    ## Reglas Generales

    - Toda operación debe validar `tenantId` y `companyId`.
    - Todo cambio crítico debe generar auditoría.
    - Todo cambio relevante debe publicar evento.
    - Los settings del módulo gobiernan validaciones y bloqueos.
    - Los catálogos gobiernan opciones seleccionables.

    ## Reglas Específicas

    - No se debe duplicar información propiedad de otros módulos.
    - Las entidades deben soportar `status`, `version`, `createdAt`, `updatedAt`.
    - Debe existir soft delete o desactivación para registros con historial.
    - El frontend oculta acciones; el backend bloquea acciones.
    """


def module_settings(m: ModuleSpec) -> str:
    return f"""
    # {m.name} — Settings y Catálogos

    ## Settings

    {md_list([f'`{s}`' for s in m.settings])}

    ## Catálogos

    Cada lista seleccionable del módulo debe provenir de `ModuleCatalog` y `ModuleCatalogOption`.

    ## Campos Configurables

    El módulo debe soportar `ModuleFieldDefinition` para campos visibles, editables, obligatorios, ordenables y validables por empresa.
    """


def module_permissions(m: ModuleSpec) -> str:
    return f"""
    # {m.name} — Permisos Granulares

    ## Permisos base

    {md_list([f'`{p}`' for p in m.permissions])}

    ## Reglas

    - Los permisos se evalúan en backend.
    - Los permisos pueden aplicar por módulo, recurso, acción y campo.
    - Los perfiles pueden replicarse entre empresas del holding.
    - Todo cambio de permiso genera auditoría.
    """


def module_apis(m: ModuleSpec) -> str:
    k = m.key.replace("_core", "").replace("_", "-")
    return f"""
    # {m.name} — APIs

    ## Convenciones

    Todas las APIs son versionadas y tenant/company scoped.

    ## Endpoints Base

    ```http
    GET /api/{k}
    POST /api/{k}
    GET /api/{k}/{{id}}
    PATCH /api/{k}/{{id}}
    POST /api/{k}/{{id}}/events
    GET /api/{k}/{{id}}/audit
    GET /api/{k}/settings/effective
    ```

    ## Errores

    - `400` validación.
    - `401` autenticación.
    - `403` autorización.
    - `404` no encontrado.
    - `409` conflicto de versión.
    - `422` regla de negocio.
    """


def module_events(m: ModuleSpec) -> str:
    return f"""
    # {m.name} — Eventos

    ## Eventos publicados

    {md_list([f'`{e}`' for e in m.events])}

    ## Contrato de Evento

    ```json
    {{
      "eventId": "uuid",
      "eventType": "{m.events[0] if m.events else 'DomainEvent'}",
      "tenantId": "tenant_001",
      "companyId": "company_001",
      "moduleKey": "{m.key}",
      "entityType": "Entity",
      "entityId": "uuid",
      "occurredAt": "2026-01-01T00:00:00Z",
      "payload": {{}}
    }}
    ```
    """


def module_workspace(m: ModuleSpec) -> str:
    return f"""
    # {m.name} — Workspace, Dashboard y KPIs

    ## Workspace estándar

    - Resumen
    - Detalle
    - Timeline
    - Documentos
    - Auditoría
    - Settings
    - Reportes

    ## Dashboard

    Debe ser configurable por perfil y empresa.

    ## KPIs

    - Total registros activos.
    - Cambios recientes.
    - Alertas abiertas.
    - Cumplimiento documental.
    - Indicadores operativos del dominio.
    """


def module_prompt(m: ModuleSpec) -> str:
    return f"""
    # {m.name} — Prompt Oficial para Cursor/Kiro

    Implementar `{m.name}` como módulo enterprise de Sentinel Logistic Truck.

    Requisitos obligatorios:

    - Multi-tenant y multi-company.
    - Settings propios.
    - Catálogos editables.
    - Permisos granulares.
    - Auditoría total.
    - APIs versionadas.
    - Eventos publicados.
    - Workspace estándar.
    - Dashboard configurable.
    - No duplicar datos de otros dominios.
    - Aplicar ownership estricto.
    - Usar Document Core para evidencias.
    - Usar Integration Hub para integraciones externas.
    """


def generate_foundations() -> None:
    folder = SLEA / "docs" / "01_Fundamentos"
    files = {
        "01A_Vision_Producto.md": """
        # 01A — Visión del Producto

        Sentinel Logistic Truck es una plataforma logística enterprise que controla el ciclo completo de la operación terrestre.

        ## Objetivos

        - Digitalizar la operación.
        - Centralizar información.
        - Eliminar planillas.
        - Controlar costos reales.
        - Medir rentabilidad.
        - Integrar GPS, TPMS, documentos, finanzas e IA.
        """,
        "01B_Filosofia_Diseno.md": """
        # 01B — Filosofía de Diseño

        El código define capacidades. La metadata define comportamiento.

        ## Principios

        - Modular Monolith.
        - API First.
        - Metadata Driven.
        - Event Driven interno.
        - Una sola base de datos.
        - Storage externo.
        """,
        "01C_Principios_Arquitectonicos.md": """
        # 01C — Principios Arquitectónicos

        - Ownership estricto.
        - Single Source of Truth.
        - Sin duplicidad de datos.
        - Auditoría total.
        - Settings por módulo.
        - Catálogos editables.
        - Permisos granulares.
        """,
        "02A_Arquitectura_General.md": """
        # 02A — Arquitectura General

        Sentinel usa Modular Monolith con módulos desacoplados por dominio, una sola base transaccional y contratos internos.
        """,
        "02B_Comunicacion_Modulos.md": """
        # 02B — Comunicación entre Módulos

        Los módulos se comunican mediante servicios internos y eventos. Nunca por acceso directo a tablas ajenas.
        """,
        "02C_Modular_Monolith.md": """
        # 02C — Modular Monolith

        Se elige por velocidad, simplicidad, menor costo operacional y capacidad de evolucionar a microservicios cuando sea necesario.
        """,
        "02D_Arquitectura_Datos.md": """
        # 02D — Arquitectura de Datos

        Una sola base de datos transaccional. Archivos externos. GPS de alto volumen puede ir a particiones o time-series.
        """,
        "03A_Convenciones.md": """
        # 03A — Convenciones

        UUID, soft delete, versionado, tenantId, companyId, auditoría y status en entidades críticas.
        """,
        "03B_Settings.md": """
        # 03B — Settings

        Todo módulo debe tener settings configurables por tenant/company y auditables.
        """,
        "03C_Catalogos.md": """
        # 03C — Catálogos

        Todo valor seleccionable debe provenir de catálogos configurables.
        """,
        "03D_Auditoria.md": """
        # 03D — Auditoría

        Todo cambio relevante registra usuario, antes, después, fecha, IP, tenant, company y motivo.
        """,
        "03E_Seguridad.md": """
        # 03E — Seguridad

        Autenticación, autorización, MFA, API Keys, sesiones, scopes y permisos granulares.
        """,
        "03F_FeatureFlags.md": """
        # 03F — Feature Flags

        Activación por tenant, company, módulo, perfil y plan comercial.
        """,
        "03G_Workspaces.md": """
        # 03G — Workspaces

        Todo módulo tendrá resumen, timeline, documentos, auditoría, settings y reportes.
        """,
        "03H_APIs.md": """
        # 03H — APIs

        REST versionado, paginación, errores estándar, idempotencia y optimistic concurrency.
        """,
        "03I_Eventos.md": """
        # 03I — Arquitectura de Eventos

        Event Dispatcher interno, eventos publicados por módulos y consumidores desacoplados.
        """,
        "03J_Checklist.md": """
        # 03J — Checklist Arquitectónico

        Todo módulo debe tener Settings, Catálogos, Auditoría, APIs, Eventos, Dashboard, Workspace, Health, KPIs y Permisos.
        """,
    }
    for name, content in files.items():
        write(folder / name, content)


def generate_module(m: ModuleSpec) -> None:
    folder = SLEA / "docs" / f"{m.number + 1:02d}_{m.key.replace('_core','').title().replace('_','')}_Core"
    docs = {
        "A_Overview.md": module_overview(m),
        "B_Data_Model.md": module_data_model(m),
        "C_Business_Rules.md": module_business_rules(m),
        "D_Settings_Catalogs.md": module_settings(m),
        "E_Permissions.md": module_permissions(m),
        "F_APIs.md": module_apis(m),
        "G_Events.md": module_events(m),
        "H_Workspace_KPIs.md": module_workspace(m),
        "I_Cursor_Kiro_Prompt.md": module_prompt(m),
    }
    for name, content in docs.items():
        write(folder / name, content)


def generate_indices() -> None:
    write(SLEA / "README.md", f"""
    # Sentinel Logistic Truck Enterprise Architecture

    Repositorio oficial de arquitectura para **Sentinel Logistic Truck (SLEA v1.0)**.

    ## Principios

    {md_list(GLOBAL_PRINCIPLES)}

    ## Módulos

    {md_list([f'{m.number}. {m.name}' for m in MODULES])}

    ## Uso

    ```bash
    python SLEA/tools/build_slea.py
    ```
    """)

    lines = ["# SUMMARY — SLEA v1.0", "", "## Volumen I — Fundamentos", ""]
    for p in sorted((SLEA / "docs" / "01_Fundamentos").glob("*.md")):
        lines.append(f"- [{p.stem}](docs/01_Fundamentos/{p.name})")
    lines.append("\n## Volumen II — Módulos Core\n")
    for m in MODULES:
        folder = f"{m.number + 1:02d}_{m.key.replace('_core','').title().replace('_','')}_Core"
        lines.append(f"### {m.name}")
        for doc in ["A_Overview.md", "B_Data_Model.md", "C_Business_Rules.md", "D_Settings_Catalogs.md", "E_Permissions.md", "F_APIs.md", "G_Events.md", "H_Workspace_KPIs.md", "I_Cursor_Kiro_Prompt.md"]:
            lines.append(f"- [{doc.replace('.md','')}](docs/{folder}/{doc})")
        lines.append("")
    write(SLEA / "SUMMARY.md", "\n".join(lines))


def generate_supporting_dirs() -> None:
    support_files = {
        "api/README.md": "# API Contracts\n\nContratos REST y DTOs por módulo.",
        "events/README.md": "# Events\n\nCatálogo de eventos publicados y consumidos.",
        "diagrams/README.md": "# Diagrams\n\nDiagramas Mermaid, ERD, BPMN y secuencia.",
        "prompts/README.md": "# Prompts\n\nPrompts oficiales para Cursor, Kiro y agentes IA.",
        "adr/README.md": "# Architecture Decision Records\n\nDecisiones de arquitectura del proyecto.",
        "templates/README.md": "# Templates\n\nPlantillas estándar de módulo, API, evento y entidad.",
    }
    for path, content in support_files.items():
        write(SLEA / path, content)


def main() -> None:
    generate_foundations()
    for module in MODULES:
        generate_module(module)
    generate_supporting_dirs()
    generate_indices()
    print("SLEA documentation generated under", SLEA)


if __name__ == "__main__":
    main()
