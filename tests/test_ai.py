from unittest.mock import patch

from fastapi.testclient import TestClient

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