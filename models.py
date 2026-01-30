# models.py
from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class TransactionModel(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    category = Column(String, index=True)
    amount = Column(Float)
    type = Column(String)
    description = Column(String, nullable=True)

# ADD THIS NEW TABLE
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) # In a real app, we would hash this!