from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field, EmailStr
from pipeline import run_research_pipeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import SessionLocal, engine
from models import Base, User, ChatHistory
from sqlalchemy.orm import Session
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token,
)

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


# database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


# PYDANTIC SCHEMAS
# auth
class SignupRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    success: bool
    access_token: str
    token_type: str


# Request body model - research
class ResearchRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=3,
        max_length=300,
        description="Research topic entered by the user",
    )


class ResearchResponse(BaseModel):
    success: bool
    data: dict


# common
class MessageResponse(BaseModel):
    success: bool
    message: str


# history
class HistoryItem(BaseModel):
    id: int
    topic: str
    created_at: str


class HistoryResponse(BaseModel):
    success: bool
    history: list[HistoryItem]


class HistoryDetailItem(BaseModel):
    id: int
    topic: str
    report: str
    feedback: str | None = None
    created_at: str


class SingleHistoryResponse(BaseModel):
    success: bool
    history: HistoryDetailItem


# ROUTES
# Health check
@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"success": True, "message": "AI Research Assistant API is running"}


# sign-up
@app.post(
    "/signup", response_model=MessageResponse, status_code=status.HTTP_201_CREATED
)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    new_user = User(
        name=data.name.strip(),
        email=data.email.lower(),
        hashed_password=hash_password(data.password),
    )

    db.add(new_user)
    db.commit()

    return {"success": True, "message": "Account created successfully."}


# login
@app.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    token = create_access_token({"sub": user.email, "user_id": user.id})
    return {"success": True, "access_token": token, "token_type": "bearer"}


# Main pipeline route
@app.post("/research")
def research(
    data: ResearchRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        topic = data.topic.strip()

        result = run_research_pipeline(topic)

        if result["status"] == "failed":
            raise HTTPException(status_code=500, detail=result["error"])

        # Get current DB user
        user = db.query(User).filter(User.email == current_user["sub"]).first()

        # Save chat history
        new_history = ChatHistory(
            user_id=user.id,
            topic=topic,
            report=result["report"],
            feedback=result["feedback"],
        )

        db.add(new_history)
        db.commit()
        db.refresh(new_history)

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# route to fetch history
@app.get("/history")
def get_history(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == current_user["sub"]).first()

    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user.id)
        .order_by(ChatHistory.created_at.desc())
        .all()
    )

    output = []

    for item in history:
        output.append(
            {
                "id": item.id,
                "topic": item.topic,
                "created_at": item.created_at.isoformat(),
            }
        )

    return {"success": True, "history": output}


# route to fetch a single report using id
@app.get("/history/{history_id}", response_model=SingleHistoryResponse)
def get_single_history(
    history_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == current_user["sub"]).first()

    item = (
        db.query(ChatHistory)
        .filter(ChatHistory.id == history_id, ChatHistory.user_id == user.id)
        .first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="History item not found.")

    return {
        "success": True,
        "history": {
            "id": item.id,
            "topic": item.topic,
            "report": item.report,
            "feedback": item.feedback,
            "created_at": item.created_at.isoformat(),
        },
    }
