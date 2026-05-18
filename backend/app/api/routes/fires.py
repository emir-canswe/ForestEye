from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.core.database import get_db
from app.models.db.models import ActiveFire
from geoalchemy2.shape import to_shape
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/active", response_model=Dict[str, Any])
def get_active_fires(db: Session = Depends(get_db)):
    """
    Son 24 saatteki aktif yangın noktalarını GeoJSON olarak döner.
    """
    twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
    fires = db.query(ActiveFire).filter(
        ActiveFire.is_active == True,
        ActiveFire.detected_at >= twenty_four_hours_ago
    ).all()
    
    features = []
    for fire in fires:
        shape = to_shape(fire.geom)
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [shape.x, shape.y]  # lon, lat
            },
            "properties": {
                "id": fire.id,
                "confidence": fire.confidence,
                "brightness": fire.brightness,
                "satellite": fire.satellite,
                "frp": fire.frp,
                "detected_at": fire.detected_at.isoformat() if fire.detected_at else None
            }
        }
        features.append(feature)
        
    return {
        "type": "FeatureCollection",
        "features": features
    }
