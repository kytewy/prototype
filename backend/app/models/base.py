"""
Base Pydantic models for the application
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class ResponseBase(BaseModel):
    """Base model for API responses"""
    success: bool = Field(True, description="Whether the request was successful")
    message: Optional[str] = Field(None, description="Response message")


class HealthCheck(ResponseBase):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.now, description="Current server time")


class ErrorResponse(ResponseBase):
    """Error response model"""
    success: bool = Field(False, description="Request was not successful")
    error_code: str = Field(..., description="Error code")
    error_details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
