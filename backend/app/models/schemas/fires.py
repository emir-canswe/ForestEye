from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActiveFireBase(BaseModel):
    detected_at: datetime
    confidence: Optional[int] = None
    brightness: Optional[float] = None
    satellite: Optional[str] = None
    frp: Optional[float] = None
    is_active: bool = True

class ActiveFireResponse(ActiveFireBase):
    id: int
    # We will format geom into lat/lon or return as GeoJSON in the router
    lat: float
    lon: float

    class Config:
        from_attributes = True
