from app.db.session import SessionLocal
from app.models.message import Message

session = SessionLocal()

message = Message(
    sender_email="john@example.com",
    subject="Duplicate payment",
    body="I think I was charged twice.",
)

session.add(message)

session.commit()

session.refresh(message)

print(message.id)