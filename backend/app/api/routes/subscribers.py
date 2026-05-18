from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.db.models import Subscriber, Subscription, GridCell
from app.models.schemas.subscribers import SubscribeRequest, SubscribeResponse
from app.core.security import get_api_key

router = APIRouter()

@router.post("/", response_model=SubscribeResponse)
def subscribe(request: SubscribeRequest, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Kullanıcıyı belirli bölgeler (GridCell) için bildirimlere abone yapar.
    """
    # Check if subscriber already exists
    subscriber = db.query(Subscriber).filter(Subscriber.email == request.email).first()
    
    if not subscriber:
        subscriber = Subscriber(
            name=request.name,
            email=request.email,
            phone=request.phone
        )
        db.add(subscriber)
        db.commit()
        db.refresh(subscriber)
    
    # Add subscriptions
    for region_id in request.regions:
        cell = db.query(GridCell).filter(GridCell.id == region_id).first()
        if not cell:
            continue
            
        # Check if already subscribed to this region
        existing_sub = db.query(Subscription).filter(
            Subscription.subscriber_id == subscriber.id,
            Subscription.grid_cell_id == region_id
        ).first()
        
        if not existing_sub:
            sub = Subscription(
                subscriber_id=subscriber.id,
                grid_cell_id=region_id,
                min_risk_level=request.min_risk_level
            )
            db.add(sub)
            
    db.commit()
    
    return SubscribeResponse(
        message="Abonelik başarıyla oluşturuldu.",
        subscriber_id=subscriber.id
    )
