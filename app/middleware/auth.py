from fastapi import Header, HTTPException, status
from typing import Optional
from app.services.app_service import AppService

async def verify_app_key(x_app_key: Optional[str] = Header(None)) -> str:
    """验证应用Key"""
    if not x_app_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-App-Key header"
        )
    
    app = AppService.get_app_by_key(x_app_key)
    if not app:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid app key"
        )
    
    return x_app_key