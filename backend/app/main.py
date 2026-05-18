from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Orman Yangını Erken Uyarı Sistemi API",
    description="Risk skoru hesaplama, yangın uyarıları ve harita entegrasyonu",
    version="1.0.0",
)

# CORS ayarları
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}

# TODO: Include routers
# from app.api.routes import risk, fires, subscribers
# app.include_router(risk.router, prefix="/v1/risk", tags=["Risk Haritası"])
# app.include_router(fires.router, prefix="/v1/fires", tags=["Aktif Yangınlar"])
# app.include_router(subscribers.router, prefix="/v1/subscribe", tags=["Abonelik"])
