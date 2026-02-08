# AI-Augmented BI Starter Platform

A runnable starter backend aligned to the BI + augmented AI requirements blueprint.

## What is included
- Semantic metric layer (single source of truth definitions)
- NL-to-SQL query translation agent (rule-based baseline)
- Row-level security (RLS) enforcement by user context
- Query execution over SQLite warehouse data
- Automated insights (trend/anomaly detection)
- Forecasting (linear baseline)
- Narrative generation for business summaries
- Human feedback capture + governance audit logging

## Project structure
- `app/main.py`: framework-agnostic service API
- `app/agents/`: task-specific AI agents
- `app/services/`: semantic layer, query execution, governance, RLS
- `scripts_seed_data.py`: creates and seeds demo warehouse
- `tests/test_service.py`: end-to-end service tests
- `docs/ai-augmented-bi-requirements.md`: requirements blueprint

## Run locally
```bash
python scripts_seed_data.py
python -m unittest discover -s tests -v
```
