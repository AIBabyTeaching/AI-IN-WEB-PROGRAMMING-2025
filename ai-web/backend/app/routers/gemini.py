"""API routes that expose Gemini-backed helpers to the frontend."""

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, constr

from app.services.gemini import GeminiServiceError, generate_lesson_outline

router = APIRouter(prefix="/ai", tags=["ai"])


logger = logging.getLogger(__name__)


class LessonOutlineIn(BaseModel):
    """Request schema describing the lesson topic submitted by the frontend."""

    topic: constr(strip_whitespace=True, min_length=1)  # type: ignore[valid-type]


class LessonOutlineOut(BaseModel):
    """Response schema returned to the frontend."""

    topic: str
    outline: list[str]


@router.post("/lesson-outline", response_model=LessonOutlineOut)
def lesson_outline(payload: LessonOutlineIn) -> LessonOutlineOut:
    """Delegate the heavy lifting to the Gemini service layer."""

    try:
        result = generate_lesson_outline(payload.topic)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except GeminiServiceError as exc:
        logger.exception("Gemini lesson outline request failed")
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return LessonOutlineOut(**result)
