import logging

import openai
from openai import OpenAI

from app.core.config import settings
from app.ai.schemas import EmailClassification
from app.core.exceptions import (
    AIAuthenticationError,
    AIConnectionError,
    AIInvalidResponseError,
    AIRateLimitError,
    AITimeoutError,
    AIUpstreamError,
)

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self) -> None:
        self._client = OpenAI(
            api_key=settings.openai_api_key,
            timeout=20.0,
            max_retries=1,
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
        import time
        started_at = time.perf_counter()
        try:
            response = self._client.responses.parse(
                model=settings.openai_model,
                input=[
                    {
                        "role": "developer",
                        "content": (
                            "You classify customer support emails. "
                            "Analyze the email according to the provided schema. "
                            "Do not invent customer or company information. "
                            "Classify based on the customer's primary goal. "
                            "Set requires_customer_lookup to true when answering "
                            "requires customer-specific account data. "
                            "Set requires_knowledge_search to true when answering "
                            "requires company policies, procedures, pricing, "
                            "product documentation, or internal knowledge. "
                            "Set requires_human_review to true for sensitive, "
                            "ambiguous, high-risk, or urgent cases. Language set as ISO 2 code standard."
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

            logger.info(
                "OpenAI classification succeeded request_id=%s model=%s",
                response._request_id,
                settings.openai_model,
            )

            classification = response.output_parsed

            if classification is None:
                raise AIInvalidResponseError()

            duration_ms = (
                                  time.perf_counter() - started_at
                          ) * 1000
            logger.info(
                "OpenAI classification succeeded "
                "request_id=%s model=%s duration_ms=%.0f",
                response._request_id,
                settings.openai_model,
                duration_ms,
            )

            return classification

        except openai.AuthenticationError as exc:
            logger.exception(
                "OpenAI authentication failed request_id=%s",
                getattr(exc, "request_id", None),
            )
            raise AIAuthenticationError() from exc

        except openai.RateLimitError as exc:
            logger.warning(
                "OpenAI rate limit reached request_id=%s",
                getattr(exc, "request_id", None),
            )
            raise AIRateLimitError() from exc

        except openai.APITimeoutError as exc:
            logger.warning(
                "OpenAI request timed out"
            )
            raise AITimeoutError() from exc

        except openai.APIConnectionError as exc:
            logger.exception(
                "OpenAI connection failed"
            )
            raise AIConnectionError() from exc

        except openai.APIStatusError as exc:
            logger.exception(
                "OpenAI API error status=%s request_id=%s",
                exc.status_code,
                exc.request_id,
            )
            raise AIUpstreamError() from exc


openai_client = OpenAIClient()