from pydantic import BaseModel
from typing import List

class FraudExplanationResponse(BaseModel):
    transaction_id: str
    explanations: List[str]
