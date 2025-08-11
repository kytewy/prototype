"""
Health check endpoints for monitoring application status
"""
from fastapi import APIRouter, Depends
from app.models.base import HealthCheck
from app.core.logging import app_logger, log_response_info
import logging

# Create router
router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)


@router.get("/ping", response_model=HealthCheck)
async def ping():
    """
    Simple health check endpoint
    
    Returns:
        HealthCheck: Health status response
    """
    response = HealthCheck(
        status="healthy",
        version="0.1.0",
    )
    
    # Log the response
    log_response_info(app_logger, 200, response.model_dump())
    
    return response
