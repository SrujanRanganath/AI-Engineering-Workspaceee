from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import Base, engine
from config import CORS_ORIGINS
import models

# Legacy tools routers (preserved for backward compatibility)
from auth.routes import router as auth_router
from tools.code_tool.routes import router as code_router
from tools.website_builder.routes import router as website_router
from tools.data_cleaner.routes import router as data_cleaner_router
from tools.document_generator.routes import router as document_router

# New Project-Centric Rebuild v1 Routers
from api.projects import router as projects_router
from api.requirements import router as requirements_router
from api.artifacts import router as artifacts_router
from api.generation import router as generation_router
from api.validation import router as validation_router

# Ensure all database tables exist and are up to date
from database import ensure_db_schema
Base.metadata.create_all(bind=engine)
ensure_db_schema()

app = FastAPI(
    title="AI Engineering Workspace",
    description="Requirement-Driven Multi-Artifact Software Generation, Integration, Validation and Repair Platform",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Legacy Tool Routers
app.include_router(auth_router)
app.include_router(code_router)
app.include_router(website_router)
app.include_router(data_cleaner_router)
app.include_router(document_router)

# Mount v1 Project Lifecycle Routers
app.include_router(projects_router)
app.include_router(requirements_router)
app.include_router(artifacts_router)
app.include_router(generation_router)
app.include_router(validation_router)

# Mount published websites for direct, safe static hosting
PUBLISHED_DIR = Path("published_websites")
PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/published", StaticFiles(directory=str(PUBLISHED_DIR), html=True), name="published")



@app.get("/")
def home():
    return {
        "message": "AI Engineering Workspace Backend Running!",
        "version": "2.0.0",
        "platform": "Requirement-Driven Multi-Artifact Engineering Platform"
    }


@app.get("/health")
def health():
    return {"status": "healthy", "service": "ai-engineering-workspace"}
