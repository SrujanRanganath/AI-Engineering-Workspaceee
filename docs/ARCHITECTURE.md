# AI Engineering Workspace — Architecture

## System Overview

The AI Engineering Workspace is a **requirement-driven, multi-artifact software engineering platform**. It takes natural-language software requirements through a structured pipeline and produces validated, testable code artifacts.

```
Natural-language requirement
  → Requirement Analysis (structured JSON)
  → Architecture Specification (schema, API contract, components)
  → Implementation Plan (phased task graph)
  → Multi-Artifact Generation (DB, backend, frontend, tests, docs)
  → Static Validation (syntax, traceability, completeness)
  → Defect Detection & Repair
  → Test Case Registration & Isolated Execution
  → Run History / Traceability
```

---

## Component Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React/TypeScript/Vite)         │
│  ProjectStudio (7 tabs)  •  Dashboard  •  Projects  •  Auth    │
│  Legacy Tools: Code, Website Builder, Data Cleaner, Docs       │
└────────────────────────┬───────────────────────────────────────┘
                         │ HTTP (REST JSON)
┌────────────────────────▼───────────────────────────────────────┐
│                        BACKEND (FastAPI)                        │
│  /api/v1/projects/*   Requirements, Spec, Plan, Gen, Validate  │
│  /api/v1/projects/*/tests/*  TestCase, TestResult, Execution   │
│  /auth/*              JWT authentication (register, login, me) │
│  /code/*  /website/*  /data-cleaner/*  /document-generator/*  │
└────────────────────────┬───────────────────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────────────────┐
│                     SERVICES LAYER                             │
│  pipeline.py:  analyze_requirement, generate_spec/plan/        │
│                generate_artifacts, validate_artifacts, repair  │
│  llm.py:       GeminiProvider / OllamaProvider / fallback      │
│  test_runner.py: Docker-isolated pytest execution              │
└────────────────────────┬───────────────────────────────────────┘
                         │ SQLAlchemy ORM
┌────────────────────────▼───────────────────────────────────────┐
│                    DATABASE (SQLite / PostgreSQL)               │
│  users  projects  requirements  artifacts  generation_runs     │
│  validation_runs  test_cases  test_results  defects            │
│  repair_attempts                                               │
└────────────────────────────────────────────────────────────────┘
```

---

## Key Design Decisions

| Decision | Rationale |
|---|---|
| FastAPI + SQLAlchemy | Async-capable, schema-validated, ORM |
| JWT authentication | Stateless, compatible with SPA frontend |
| Docker test isolation | Generated code is untrusted; no host execution |
| Deterministic pipeline fallback | Tests cannot call Gemini; fallback ensures determinism |
| Pydantic v2 schemas | Strict request/response validation |
| SQLite default | Zero-setup for local development |

---

## Data Models

| Model | Key Fields |
|---|---|
| `User` | id, email, hashed_password |
| `Project` | id, user_id, name, description, status |
| `Requirement` | id, project_id, raw_text, structured (JSON), status, version |
| `Artifact` | id, project_id, artifact_type, name, path, content, version, status, generation_run_id, requirement_id |
| `GenerationRun` | id, project_id, operation, status, provider, model, started_at, completed_at, error, input_metadata, output_metadata |
| `ValidationRun` | id, project_id, artifact_id, check_type, status, message, details |
| `TestCase` | id, project_id, artifact_id, requirement_id, name, description, test_type, status |
| `TestResult` | id, test_case_id, status, output, duration_ms, executed_at |
| `Defect` | id, project_id, artifact_id, validation_run_id, test_result_id, severity, description, status |
| `RepairAttempt` | id, defect_id, strategy, patch, status, result_message |

---

## LLM Provider Abstraction

`services/llm.py` provides a provider-agnostic `ask_llm()` function.

- **Gemini**: Used when `GEMINI_API_KEY` is configured
- **Ollama**: Used when explicitly configured (`OLLAMA_*` env vars)
- **Fallback**: All pipeline functions have deterministic fallbacks; LLM failure does not crash the pipeline

> The fallback never fabricates realistic AI output — it produces structurally valid but template-based data.
