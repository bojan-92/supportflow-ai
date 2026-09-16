from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


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