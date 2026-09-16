from fastapi import APIRouter

from app.ai.client import openai_client
from app.ai.schemas import AIRequest, AIResponse


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/test",
    response_model=AIResponse,
)
def test_ai(request: AIRequest) -> AIResponse:
    response_text = openai_client.generate_text(
        request.message,
    )

    return AIResponse(
        response=response_text,
    )