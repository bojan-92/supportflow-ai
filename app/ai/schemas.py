from enum import Enum
from pydantic import BaseModel, Field


class AIRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000,
    )


class AIResponse(BaseModel):
    response: str

class Intent(str, Enum):
    BILLING = "BILLING"
    REFUND = "REFUND"
    TECH_SUPPORT = "TECH_SUPPORT"
    ACCOUNT = "ACCOUNT"
    ORDER_STATUS = "ORDER_STATUS"
    CANCELLATION = "CANCELLATION"
    SALES = "SALES"
    GENERAL = "GENERAL"
    SPAM = "SPAM"
    OTHER = "OTHER"


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class Sentiment(str, Enum):
    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"


class EmailClassificationRequest(BaseModel):
    subject: str = Field(
        default="",
        max_length=500,
    )

    body: str = Field(
        min_length=1,
        max_length=10000,
    )


class EmailClassification(BaseModel):
    intent: Intent

    priority: Priority

    sentiment: Sentiment

    language: str = Field(
        min_length=2,
        max_length=20,
    )

    requires_customer_lookup: bool

    requires_knowledge_search: bool

    requires_human_review: bool

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )