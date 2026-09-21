from openai import OpenAI

from app.core.config import settings
from app.ai.schemas import EmailClassification

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

    def classify_email(
            self,
            subject: str,
            body: str,
    ) -> EmailClassification:
        response = self._client.responses.parse(
            model=settings.openai_model,
            input=[
                {
                    "role": "developer",
                    "content": (
                        "You classify customer support emails. "
                        "Analyze the email according to the provided schema. "
                        "Do not invent customer or company information. "
                        "Set requires_customer_lookup to true when answering "
                        "would require customer-specific account data. "
                        "Set requires_knowledge_search to true when answering "
                        "would require company policies, procedures, pricing, "
                        "product documentation, or other internal knowledge. "
                        "Set requires_human_review to true for sensitive, "
                        "ambiguous, high-risk, or urgent cases. Language put as ISO 2 chars standard value."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Subject: {subject}\n\n"
                        f"Email body:\n{body}"
                    ),
                },
            ],
            text_format=EmailClassification,
        )

        classification = response.output_parsed

        if classification is None:
            raise RuntimeError(
                "OpenAI did not return a parsed classification."
            )

        return classification


openai_client = OpenAIClient()