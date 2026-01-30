from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from pydantic import BaseModel

import models
from database import SessionLocal, engine, get_db

# Create the tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Muttha Sales API")

# VERY IMPORTANT: This allows your HTML file to send data to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This is for reading the data coming FROM your dashboard
class TransactionSchema(BaseModel):
    date: date
    category: str
    amount: float
    type: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

@app.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    return db.query(models.TransactionModel).all()

@app.post("/transactions")
def create_transaction(item: TransactionSchema, db: Session = Depends(get_db)):
    db_item = models.TransactionModel(
        date=item.date,
        category=item.category,
        amount=item.amount,
        type=item.type,
        description=item.description
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"status": "success", "id": db_item.id}

# main.py updates
class LoginSchema(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(models.UserModel).filter(models.UserModel.username == data.username).first()
    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"status": "success", "message": "Welcome back!"}

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Delete a specific transaction by its ID."""
    db_item = db.query(models.TransactionModel).filter(models.TransactionModel.id == transaction_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(db_item)
    db.commit()
    return {"status": "success", "message": "Transaction deleted"}