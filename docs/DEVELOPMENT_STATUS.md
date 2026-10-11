# AI Engineering Workspace — Development Status

> Last updated: 2026-10-06

## Current State: MVP Complete

---

## What Is Implemented

### Backend (FastAPI / SQLAlchemy)

| Feature | Status | Notes |
|---|---|---|
| JWT Authentication | ✅ Complete | Register, login, /me |
| Project CRUD | ✅ Complete | Ownership isolation |
| Requirement CRUD + Analysis | ✅ Complete | LLM + deterministic fallback |
| Architecture Specification | ✅ Complete | LLM + template fallback |
| Implementation Plan | ✅ Complete | LLM + template fallback |
| Multi-Artifact Generation (5 tiers) | ✅ Complete | Deterministic templates |
| Artifact CRUD | ✅ Complete | Manual create/update supported |
| Static Validation | ✅ Complete | AST syntax, traceability, completeness |
| Defect Detection | ✅ Complete | Persists Defect records |
| Automated Repair | ✅ Complete | LLM repair + fallback stub |
| TestCase Registration | ✅ Complete | Linked to artifact + requirement |
| TestResult Persistence | ✅ Complete | Persisted per run |
| Docker-Isolated Test Execution | ✅ Complete | `runner_unavailable` if Docker absent |
| Generation Run History | ✅ Complete | Full audit trail |
| Legacy Tools | ✅ Complete | /code, /website, /data-cleaner, /document-generator |

### Frontend (React/TypeScript/Vite)

| Feature | Status | Notes |
|---|---|---|
| Authentication (Login/Register) | ✅ Complete | JWT stored, protected routes |
| Projects List Page | ✅ Complete | Create, browse, navigate |
| ProjectStudio — Requirements | ✅ Complete | NL input, structured breakdown |
| ProjectStudio — Specification | ✅ Complete | Schema, API contract, security model |
| ProjectStudio — Plan | ✅ Complete | Phased task graph |
| ProjectStudio — Artifacts | ✅ Complete | Code viewer, copy, export |
| ProjectStudio — Validation | ✅ Complete | Scorecard, defect list, repair |
| ProjectStudio — Tests | ✅ Complete | TestCase CRUD, run, result display |
| ProjectStudio — Run History | ✅ Complete | Audit log of all LLM runs |
| Legacy Tool Pages | ✅ Preserved | Code, Website, Docs, Data tools |

### Testing

| Suite | Status |
|---|---|
| Backend unit tests | ✅ 13/13 passing |
| LLM-free (deterministic) | ✅ All tests mock/stub LLM |
| Frontend build | ✅ TypeScript clean, Vite build passes |

---

## Known Limitations

### Must-Fix Before Production

1. **JWT revocation not implemented** — tokens cannot be invalidated before expiry
2. **SQLite write concurrency** — single writer; use PostgreSQL for concurrent users
3. **No rate limiting** — add nginx/API gateway rate limiting in production
4. **CORS `["*"]`** — set specific origins in `.env` for production deployment

### Honest About What Isn't Done

| Feature | Status | Notes |
|---|---|---|
| LLM-generated code quality | ⚠️ Template-based fallback | Real LLM output requires valid `GEMINI_API_KEY` |
| Docker runner image pre-build | ⚠️ Must be built first | `runner_unavailable` returned until image exists |
| Frontend real-time updates | ❌ Not implemented | Page refresh required for state changes |
| Audit log UI | ❌ Not implemented | GenerationRun history available via API |
| Role-based access control | ❌ Not implemented | Single user per account |
| Multi-user project sharing | ❌ Not implemented | Projects are private per user |
| Requirement version history | ❌ Partial | Version field exists; no diff UI |

---

## How to Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Run Backend Tests
```bash
cd backend
python -m unittest tests.test_v1_api -v
```

### Docker Test Runner Image (optional — for test execution)
```bash
# The image is auto-built on first test run if Docker is available
# To pre-build manually:
docker build -t ai-engineering-workspace-test-runner:py312-pytest8.3.5 - <<'EOF'
FROM python:3.12.8-slim-bookworm
RUN python -m pip install --no-cache-dir pytest==8.3.5 SQLAlchemy==2.0.36 pydantic==2.10.4 fastapi==0.115.6
RUN useradd --uid 10001 --create-home runner
USER 10001:10001
WORKDIR /tmp
EOF
```

---

## Recommended Next Tasks

1. **PostgreSQL migration** — replace SQLite with PostgreSQL for production
2. **Frontend polling / WebSocket** — live pipeline status updates
3. **Requirement version diff** — show changes between requirement versions
4. **LLM context improvement** — include project history in prompts for better generation
5. **RBAC** — admin/viewer/editor roles per project
6. **Docker image CI** — pre-build runner image in CI and push to registry
7. **Lint / pre-commit hooks** — enforce code quality on commits
8. **Multi-tenant project sharing** — invite collaborators to projects
