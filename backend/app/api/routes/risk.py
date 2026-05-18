from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.core.database import get_db
from app.models.db.models import GridCell, RiskScore
from app.models.schemas.risk import GridCellResponse, RiskScoreResponse
from geoalchemy2.shape import to_shape
import json

router = APIRouter()

@router.get("/current", response_model=Dict[str, Any])
def get_current_risk(
    min_score: int = Query(0, description="Minimum risk skoru filtresi"),
    risk_level: str = Query("all", description="low/medium/high/critical"),
    il: Optional[str] = Query(None, description="İl adına göre filtre"),
    db: Session = Depends(get_db)
):
    """
    Tüm grid hücrelerinin güncel risk skorlarını GeoJSON formatında döner.
    """
    # This is a simplified query. In reality, we want the *latest* risk score per cell.
    # We can do this by querying RiskScore directly or GridCell joined with its latest risk.
    query = db.query(GridCell)
    
    if il:
        query = query.filter(GridCell.il_adi == il)
        
    cells = query.all()
    
    features = []
    for cell in cells:
        # Get the latest risk score for this cell
        latest_risk = db.query(RiskScore).filter(RiskScore.grid_cell_id == cell.id).order_by(RiskScore.calculated_at.desc()).first()
        
        if not latest_risk:
            continue
            
        if latest_risk.risk_score < min_score:
            continue
            
        if risk_level != "all" and latest_risk.risk_level != risk_level:
            continue
            
        # Convert WKB geometry to GeoJSON
        shape = to_shape(cell.geom)
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [list(shape.exterior.coords)]
            },
            "properties": {
                "cell_id": cell.id,
                "il_adi": cell.il_adi,
                "ilce_adi": cell.ilce_adi,
                "risk_score": latest_risk.risk_score,
                "risk_level": latest_risk.risk_level,
                "humidity": latest_risk.humidity,
                "wind_speed": latest_risk.wind_speed,
                "temperature": latest_risk.temperature,
                "calculated_at": latest_risk.calculated_at.isoformat() if latest_risk.calculated_at else None
            }
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "generated_at": datetime.utcnow().isoformat() if features else None,
        "features": features
    }

@router.get("/cell/{cell_id}", response_model=Dict[str, Any])
def get_cell_detail(cell_id: int, db: Session = Depends(get_db)):
    """
    Belirli bir hücrenin detayını döner (Geçmiş risk trendi vb.)
    """
    cell = db.query(GridCell).filter(GridCell.id == cell_id).first()
    if not cell:
        raise HTTPException(status_code=404, detail="Grid cell not found")
        
    # Get last 24 hours of risk scores
    scores = db.query(RiskScore).filter(RiskScore.grid_cell_id == cell_id).order_by(RiskScore.calculated_at.desc()).limit(24).all()
    
    return {
        "cell_id": cell.id,
        "il_adi": cell.il_adi,
        "ilce_adi": cell.ilce_adi,
        "lat": cell.lat_center,
        "lon": cell.lon_center,
        "history": [
            {
                "calculated_at": s.calculated_at.isoformat(),
                "risk_score": s.risk_score,
                "risk_level": s.risk_level,
                "humidity": s.humidity,
                "wind_speed": s.wind_speed,
                "temperature": s.temperature
            } for s in scores
        ]
    }
