from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, BigInteger, Date, CheckConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from .base import Base

class GridCell(Base):
    __tablename__ = "grid_cells"

    id = Column(Integer, primary_key=True, autoincrement=True)
    geom = Column(Geometry('POLYGON', srid=4326), nullable=False)
    lat_center = Column(Float, nullable=False)
    lon_center = Column(Float, nullable=False)
    il_adi = Column(String(50))
    ilce_adi = Column(String(100))
    elevation = Column(Integer)
    slope = Column(Float)
    aspect = Column(Float)

    risk_scores = relationship("RiskScore", back_populates="grid_cell", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="grid_cell", cascade="all, delete-orphan")

class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    grid_cell_id = Column(Integer, ForeignKey("grid_cells.id"))
    calculated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(10), nullable=False)
    humidity = Column(Float)
    wind_speed = Column(Float)
    wind_deg = Column(Float)
    temperature = Column(Float)
    ndvi = Column(Float)
    dry_days = Column(Integer)
    model_version = Column(String(20), default="rule_v1")

    grid_cell = relationship("GridCell", back_populates="risk_scores")

    __table_args__ = (
        CheckConstraint('risk_score >= 0 AND risk_score <= 100', name='check_risk_score_range'),
        Index('idx_risk_scores_cell_time', 'grid_cell_id', 'calculated_at', postgresql_ops={'calculated_at': 'DESC'}),
    )

class ActiveFire(Base):
    __tablename__ = "active_fires"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    geom = Column(Geometry('POINT', srid=4326), nullable=False)
    detected_at = Column(DateTime(timezone=True), nullable=False)
    confidence = Column(Integer)
    brightness = Column(Float)
    satellite = Column(String(30))
    frp = Column(Float)
    is_active = Column(Boolean, default=True)

class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    phone = Column(String(20))
    fcm_token = Column(String(500))
    subscribed_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    subscriptions = relationship("Subscription", back_populates="subscriber", cascade="all, delete-orphan")
    notifications = relationship("NotificationSent", back_populates="subscriber", cascade="all, delete-orphan")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"))
    grid_cell_id = Column(Integer, ForeignKey("grid_cells.id"))
    min_risk_level = Column(String(10), default="high")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    subscriber = relationship("Subscriber", back_populates="subscriptions")
    grid_cell = relationship("GridCell", back_populates="subscriptions")

class NotificationSent(Base):
    __tablename__ = "notifications_sent"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"))
    risk_score_id = Column(BigInteger, ForeignKey("risk_scores.id"))
    channel = Column(String(20))
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20))
    provider_id = Column(String(200))

    subscriber = relationship("Subscriber", back_populates="notifications")

class HistoricalFire(Base):
    __tablename__ = "historical_fires"

    id = Column(Integer, primary_key=True, autoincrement=True)
    geom = Column(Geometry('POINT', srid=4326), nullable=False)
    fire_date = Column(Date, nullable=False)
    il_adi = Column(String(50))
    hectares_burned = Column(Float)
    cause = Column(String(100))
    source = Column(String(50), default="OGM")
