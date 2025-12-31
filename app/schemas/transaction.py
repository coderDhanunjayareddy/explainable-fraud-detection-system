from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    transaction_id: str = Field(..., example="TXN12345")
    amount: float = Field(..., gt=0, example=15000.75)
    department: str = Field(..., example="Public Works")
    vendor: str = Field(..., example="ABC Infra Pvt Ltd")
    transaction_date: datetime
    description: Optional[str] = Field(None, example="Road maintenance payment")

class TransactionResponse(TransactionBase):
    fraud_score: Optional[float] = Field(None, example=0.82)
    is_suspicious: Optional[bool] = Field(None, example=True)
