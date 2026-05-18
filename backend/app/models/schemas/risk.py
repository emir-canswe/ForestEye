from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RiskScoreBase(BaseModel):
    risk_score: float
    risk_level: str
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_deg: Optional[float] = None
    temperature: Optional[float] = None
    ndvi: Optional[float] = None
    dry_days: Optional[int] = None

class RiskScoreResponse(RiskScoreBase):
    id: int
    grid_cell_id: int
    calculated_at: datetime
    
    class Config:
        from_attributes = True

class GridCellResponse(BaseModel):
    id: int
    lat_center: float
    lon_center: float
    il_adi: Optional[str] = None
    ilce_adi: Optional[str] = None
    # Latest risk score can be included if joined
    latest_risk: Optional[RiskScoreResponse] = None

    class Config:
        from_attributes = True
