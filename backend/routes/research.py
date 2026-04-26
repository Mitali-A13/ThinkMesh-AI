from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.routes.deps import get_db, get_current_user, get_db_user

from backend.schemas.research import ResearchRequest, ResearchResponse

from backend.db.models import ChatHistory
from backend.services.pipeline_service import generate_research

router = APIRouter(tags=["Research"])


# Main pipeline route
@router.post("/research")
def research(
    data: ResearchRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        topic = data.topic.strip()

        result = generate_research(topic)

        if result["status"] == "failed":
            raise HTTPException(status_code=500, detail=result["error"])

        # Get current DB user
        user = get_db_user(current_user, db)

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
