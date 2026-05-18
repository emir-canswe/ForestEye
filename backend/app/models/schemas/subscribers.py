from pydantic import BaseModel, EmailStr
from typing import Optional, List

class SubscribeRequest(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    regions: List[int]  # List of grid_cell_ids
    min_risk_level: str = "high"

class SubscribeResponse(BaseModel):
    message: str
    subscriber_id: int
