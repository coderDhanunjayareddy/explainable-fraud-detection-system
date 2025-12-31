from pydantic import BaseModel
from datetime import datetime

class FraudResultResponse(BaseModel):
    transaction_id: str
    amount: float
    vendor: str
    department: str
    transaction_date: datetime
    fraud_score: float
    is_suspicious: bool
    source_transaction_ref: str | None

