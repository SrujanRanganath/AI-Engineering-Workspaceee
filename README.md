# 🚀 AI Engineering Workspace Using Multi-Agent Systems

An enterprise-grade, requirement-driven AI engineering workspace featuring a **FastAPI** backend, **React + TypeScript + Vite** frontend, **Multi-Agent Orchestration Pipeline**, and automated verification/repair workflows.

---

## 📌 Project Overview

**AI Engineering Workspace Using Multi-Agent Systems** is a modular engineering platform developed as a Final Year Engineering Project.

The platform provides:
1. **Core AI Engineering Tools**: Code Generation & Explanation, Multi-File Website Building, DOCX Document Generation, and Dataset Cleaning.
2. **Project-Centric Multi-Agent Lifecycle**: Requirement ingestion, architectural planning, multi-artifact generation, integration, static verification, test execution, defect detection, and repair.
3. **Enterprise Security**: Path traversal confinement, role/owner isolated access, safe project export, and sandboxed validation.

---

## 👩‍💻 Authors & Attributions

* **Tejaswini S** — *Original Project Architecture & Core AI Tool Implementation* (Final Year Engineering Project)
* **Srujan Ranganath** — *Multi-Agent Architecture, Verification Pipeline, Security Controls, and Full-Stack Monorepo Integration*

---

## 🛠 Tech Stack

### Backend
* **FastAPI** (v2.0.0 Architecture)
* **Python 3.12+**
* **SQLAlchemy ORM** (SQLite default, PostgreSQL configurable)
* **Pydantic v2**
* **JWT Authentication & Passlib/Bcrypt**
* **Google Gemini AI API** (with resilient offline/mock fallback)
* **pandas, python-docx, openpyxl**

### Frontend
* **React 18**
* **TypeScript**
* **Vite**
* **Tailwind CSS & Lucide Icons**

### Testing & Verification
* **pytest** test suite
* **Static Test Verifier** (AST analysis, syntax validation)
* **File Path Security Suite** (Path traversal defenses)

---

## 📂 Project Structure

```text
AI-Engineering-Workspace/
├── backend/                  # FastAPI 2.0 Backend Application
│   ├── api/                  # Project Lifecycle v1 Routers (projects, requirements, artifacts, etc.)
│   ├── auth/                 # JWT Authentication, password hashing, dependencies
│   ├── models/               # SQLAlchemy ORM Models (User, Project, Requirement, Artifact, etc.)
│   ├── services/             # Pipeline orchestration, LLM service, test runners, verifiers
│   ├── tests/                # Automated pytest suite (40+ unit and security tests)
│   ├── tools/                # 4 Core AI Tools (code_tool, website_builder, data_cleaner, document_generator)
│   ├── utils/                # Security utils (path containment, filename sanitation)
│   ├── config.py             # Backend configuration and environment management
│   ├── database.py           # Database engine, session maker, schema migration
│   ├── main.py               # FastAPI application entry point
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Backend environment template
│
├── frontend/                 # React + TypeScript + Vite Web Application
│   ├── src/
│   │   ├── api/              # API client and mock services
│   │   ├── components/       # Shared UI components (Navbar, ProtectedRoute, CodeViewer, etc.)
│   │   ├── context/          # Auth and Toast contexts
│   │   ├── pages/            # Dashboard, Projects, ProjectStudio, and Tool pages
│   │   └── types/            # TypeScript interfaces and data contracts
│   ├── package.json          # Node dependencies
│   └── vite.config.ts        # Vite configuration
│
├── docs/                     # Comprehensive Project Documentation
│   ├── ARCHITECTURE.md       # Multi-agent system architecture & component diagrams
│   ├── SECURITY.md           # Threat model, path traversal controls, and audit records
│   ├── API_WORKFLOW.md       # Complete REST API lifecycle documentation
│   └── DEVELOPMENT_STATUS.md # Milestone and feature implementation status
│
├── main.py                   # Root entry point bridging directly to backend.main:app
├── requirements.txt          # Root Python dependencies reference
├── API_DOCUMENTATION.md      # Legacy REST API reference
├── HANDOVER_GUIDE.md         # Operational handover documentation
├── README.md                 # Project README
└── .gitignore                # Unified monorepo ignore rules
```

---

## ✨ Features & Tools

### 1. 💻 AI Code Tool
* Multi-language code generation (Python, JavaScript, TypeScript, Go, Java, C++, Rust).
* Code explanation and architectural rationale.
* Project save, static syntax verification, and ZIP download.

### 2. 🌐 AI Website Builder
* Multi-file website generation (HTML, CSS, JavaScript).
* Live interactive preview.
* Safe static publishing to `/published/{project_name}/index.html`.
* One-click ZIP download.

### 3. 📄 AI Document Generator
* Professional DOCX document generation.
* Standard templates: Resumes, Cover Letters, Statement of Purpose (SOP), and Technical Project Reports.
* Downloadable Word artifacts.

### 4. 🧹 AI Data Cleaner
* Upload and analyze CSV datasets.
* Automated missing value imputation, duplicate removal, and data type formatting.
* Before/after data quality summary reports and CSV export.

### 5. 🤖 Multi-Agent Project Lifecycle
* **Requirements Agent**: Parse and structure functional specifications.
* **Architecture & Planning Agent**: Decompose requirements into executable engineering tasks.
* **Artifact Generation Agent**: Generate modular source code, configurations, and assets.
* **Validation & Testing Agent**: Static analysis and automated test case execution.
* **Defect & Repair Agent**: Automated defect diagnosis and repair cycle.

---

## ⚙ Installation & Setup

### 1. Prerequisites
* Python 3.12+
* Node.js v18+ & npm v9+

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and configure SECRET_KEY and GEMINI_API_KEY
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment (optional, defaults to http://127.0.0.1:8000)
cp .env.example .env
```

---

## ▶ Running the Application

### Start the Backend
```bash
# From the repository root:
python main.py
# Or from backend directory:
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
* API Server: `http://127.0.0.1:8000`
* Interactive API Documentation (Swagger): `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

### Start the Frontend
```bash
cd frontend
npm run dev
```
* Frontend Application: `http://localhost:5173`

---

## 🧪 Testing

Run the automated backend test suite:
```bash
cd backend
pytest tests/ -v
```
All 40+ unit, integration, and security tests pass out of the box with zero failures.

---

## 🔒 Security Architecture

* **Path Traversal Protection**: All user file access and downloads are strictly confined to authorized subdirectories using `os.path.commonpath` verification.
* **Cross-User Isolation**: Projects, artifacts, and test runs are isolated by user ownership.
* **Zero Host Execution Risk**: Arbitrary user/generated code is analyzed statically via Python AST checks without executing unverified code directly on the host.

---

## 📄 License

Developed for academic and educational purposes under the Final Year Engineering Curriculum.
