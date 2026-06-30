# Sentinel Logistic Truck

Repositorio base para la arquitectura y posterior implementación de **Sentinel Logistic Truck**.

## Enfoque

Este repositorio no busca acumular cientos de documentos dispersos. La estrategia oficial es mantener **pocos documentos de arquitectura ejecutable**, con directrices claras para que Cursor/Kiro bajen la implementación módulo a módulo.

## Documentos principales

- `SLEA/00_ARCHITECTURE_DIRECTIVES.md` — Constitución técnica del proyecto.
- `SLEA/01_DELIVERY_REQUIREMENTS.md` — Qué debe entregar Cursor/Kiro por cada módulo.
- `SLEA/02_MODULE_BLUEPRINTS.md` — Blueprint funcional de todos los módulos aprobados.
- `SLEA/03_CURSOR_EXECUTION_PROMPT.md` — Prompt maestro operativo para Cursor/Kiro.

## Principios

- Modular Monolith.
- Una sola base de datos.
- Multi-tenant y multi-company.
- Módulos activables por empresa.
- Metadata Driven.
- API First.
- Event Driven interno.
- Document Core transversal.
- Storage externo para archivos.
- Settings, catálogos, permisos, auditoría y health en todos los módulos.

## Regla suprema

La arquitectura manda. Si una implementación funciona pero rompe la arquitectura, se rechaza.
