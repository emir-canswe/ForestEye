from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """
    Basit API Key doğrulaması. 
    Kritik endpoint'ler (POST/PUT/DELETE) için kullanılır.
    """
    # MVP aşaması için sabit bir API key kabul edelim
    # Production'da veritabanından veya Hashicorp Vault'tan kontrol edilebilir.
    expected_api_key = settings.SECRET_KEY 
    
    if api_key_header == expected_api_key:
        return api_key_header
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate API key"
    )
