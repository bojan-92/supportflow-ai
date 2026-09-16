from openai import OpenAI

from app.core.config import settings


class OpenAIClient:
    def __init__(self) -> None:
        self._client = OpenAI(
            api_key=settings.openai_api_key,
        )

    def generate_text(
        self,
        message: str,
    ) -> str:
        response = self._client.responses.create(
            model=settings.openai_model,
            instructions=(
                "You are a customer support assistant for SupportFlow. "
                "Answer in at most two sentences. "
                "Never invent company policies. "
                "If company-specific information is required, say that "
                "you do not have enough information."
            ),
            input=message,
        )

        return response.output_text


openai_client = OpenAIClient()