"""API routes that expose Gemini-backed helpers to the frontend."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.gemini import GeminiServiceError, generate_lesson_outline

router = APIRouter(prefix="/ai", tags=["ai"])


class LessonOutlineIn(BaseModel):
    """Request schema describing the lesson topic submitted by the frontend."""

    topic: str


class LessonOutlineOut(BaseModel):
    """Response schema returned to the frontend."""

    topic: str
    outline: list[str]


@router.post("/lesson-outline", response_model=LessonOutlineOut)
def lesson_outline(payload: LessonOutlineIn) -> LessonOutlineOut:
    """Delegate the heavy lifting to the Gemini service layer."""

    try:
        result = generate_lesson_outline(payload.topic)
    except GeminiServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return LessonOutlineOut(**result)
