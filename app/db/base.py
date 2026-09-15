from sqlalchemy.orm import DeclarativeBase

# this is root of all DB model classes like Message, Customer, Ticket...
class Base(DeclarativeBase):
    pass