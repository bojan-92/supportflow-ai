from unittest.mock import patch
import openai
from fastapi.testclient import TestClient
from app.core.exceptions import AITimeoutError
from app.core.exceptions import AIRateLimitError
from app.core.exceptions import AIInvalidResponseError

from app.main import app
from app.ai.schemas import (
    EmailClassification,
    Intent,
    Priority,
    Sentiment,
)


client = TestClient(app)


def test_ai_endpoint_returns_response():
    with patch(
        "app.api.ai.openai_client.generate_text",
        return_value="This is a test response.",
    ):
        response = client.post(
            "/ai/test",
            json={
                "message": "I was charged twice."
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "response": "This is a test response."
    }

def test_ai_endpoint_rejects_empty_message():
    response = client.post(
        "/ai/test",
        json={
            "message": ""
        },
    )

    assert response.status_code == 422

def test_classify_email():
    classification = EmailClassification(
        intent=Intent.BILLING,
        priority=Priority.MEDIUM,
        sentiment=Sentiment.NEGATIVE,
        language="en",
        requires_customer_lookup=True,
        requires_knowledge_search=True,
        requires_human_review=True,
        confidence=0.97,
    )

    with patch(
        "app.api.ai.openai_client.classify_email",
        return_value=classification,
    ):
        response = client.post(
            "/ai/classify",
            json={
                "subject": "Charged twice",
                "body": "I was charged twice.",
            },
        )

    assert response.status_code == 200

    assert response.json() == {
        "intent": "BILLING",
        "priority": "MEDIUM",
        "sentiment": "NEGATIVE",
        "language": "en",
        "requires_customer_lookup": True,
        "requires_knowledge_search": True,
        "requires_human_review": True,
        "confidence": 0.97,
    }

def test_classify_email_rejects_empty_body():
    response = client.post(
        "/ai/classify",
        json={
            "subject": "Hello",
            "body": "",
        },
    )

    assert response.status_code == 422

def test_classify_returns_503_on_ai_timeout():
    with patch(
        "app.api.ai.openai_client.classify_email",
        side_effect=AITimeoutError(),
    ):
        response = client.post(
            "/ai/classify",
            json={
                "subject": "Charged twice",
                "body": "I was charged twice.",
            },
        )

    assert response.status_code == 503

    body = response.json()

    assert body["code"] == "AI_TIMEOUT"
    assert (
        body["message"]
        == "AI processing timed out. Please try again."
    )

    assert body["request_id"].startswith("sf_")

def test_classify_returns_503_on_rate_limit():
    with patch(
        "app.api.ai.openai_client.classify_email",
        side_effect=AIRateLimitError(),
    ):
        response = client.post(
            "/ai/classify",
            json={
                "subject": "Refund",
                "body": "I want a refund.",
            },
        )

    assert response.status_code == 503

    assert response.json()["code"] == "AI_RATE_LIMITED"

def test_classify_returns_503_on_invalid_ai_response():
    with patch(
        "app.api.ai.openai_client.classify_email",
        side_effect=AIInvalidResponseError(),
    ):
        response = client.post(
            "/ai/classify",
            json={
                "subject": "Something",
                "body": "Please help me.",
            },
        )

    assert response.status_code == 503

    assert response.json()["code"] == "AI_INVALID_RESPONSE"

def test_unexpected_error_returns_500():
    error_client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    with patch(
        "app.api.ai.openai_client.classify_email",
        side_effect=RuntimeError("boom"),
    ):
        response = error_client.post(
            "/ai/classify",
            json={
                "subject": "Something",
                "body": "Please help me.",
            },
        )

    assert response.status_code == 500

    body = response.json()

    assert body["code"] == "INTERNAL_SERVER_ERROR"

    assert body["message"] == (
        "An unexpected error occurred."
    )

    assert body["request_id"].startswith("sf_")

    assert "boom" not in body["message"]
