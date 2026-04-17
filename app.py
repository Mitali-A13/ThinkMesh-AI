from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from pipeline import run_research_pipeline
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="AI Research Assistant API",
    version="1.0.0",
    description="API for generating AI-powered research reports using multi-agent pipeline.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request body model
class ResearchRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=3,
        max_length=300,
        description="Research topic entered by the user",
    )


# Health check
@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"success": True, "message": "AI Research Assistant API is running"}


# Main pipeline route
@app.post("/research", status_code=status.HTTP_200_OK)
def research(data: ResearchRequest):
    try:
        topic = data.topic.strip()

        if not topic:
            raise HTTPException(status_code=400, detail="Topic cannot be empty.")

        result = run_research_pipeline(topic)

        if result["status"] == "failed":
            raise HTTPException(status_code=500, detail=result["error"])

        return {"success": True, "data": result}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
