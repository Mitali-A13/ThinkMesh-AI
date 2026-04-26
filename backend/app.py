from fastapi import FastAPI, HTTPException, status, Depends
from backend.pipeline import run_research_pipeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.db.database import SessionLocal, engine
from backend.db.models import Base, User, ChatHistory
from sqlalchemy.orm import Session
from backend.schemas.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
    ChangePasswordRequest,
    MeResponse,
)
from backend.schemas.research import (
    ResearchRequest,
    ResearchResponse,
)
from backend.schemas.history import (
    MessageResponse,
    HistoryResponse,
    SingleHistoryResponse,
)
from backend.auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token,
)
from backend.routes.auth import router as auth_router
from backend.routes.research import router as research_router
from backend.routes.history import router as history_router


# create DB tables
Base.metadata.create_all(bind=engine)

# app config
app = FastAPI(
    title="AI Research Assistant API",
    version="1.0.0",
    description="API for generating AI-powered research reports using multi-agent pipeline.",
)

security = HTTPBearer()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ROUTES
# Health check
@app.get("/")
def home():
    return {"success": True, "message": "API is running"}


app.include_router(auth_router)
app.include_router(research_router)
app.include_router(history_router)
