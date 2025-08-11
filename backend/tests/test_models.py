"""
Tests for Pydantic models
"""
from datetime import datetime
from pydantic import ValidationError
import pytest

from app.models.base import ResponseBase, HealthCheck, ErrorResponse


def test_response_base_model():
    """Test ResponseBase model validation"""
    # Test with valid data
    response = ResponseBase(success=True, message="Test message")
    assert response.success is True
    assert response.message == "Test message"
    
    # Test with default values
    response = ResponseBase()
    assert response.success is True
    assert response.message is None


def test_health_check_model():
    """Test HealthCheck model validation"""
    # Test with valid data
    health = HealthCheck(status="healthy", version="1.0.0")
    assert health.status == "healthy"
    assert health.version == "1.0.0"
    assert health.success is True
    assert isinstance(health.timestamp, datetime)
    
    # Test with missing required fields
    with pytest.raises(ValidationError):
        HealthCheck(success=True)


def test_error_response_model():
    """Test ErrorResponse model validation"""
    # Test with valid data
    error = ErrorResponse(error_code="NOT_FOUND", message="Resource not found")
    assert error.success is False
    assert error.error_code == "NOT_FOUND"
    assert error.message == "Resource not found"
    assert error.error_details is None
    
    # Test with error details
    details = {"field": "id", "reason": "Invalid format"}
    error = ErrorResponse(
        error_code="VALIDATION_ERROR",
        message="Validation failed",
        error_details=details
    )
    assert error.error_details == details
    
    # Test with missing required fields
    with pytest.raises(ValidationError):
        ErrorResponse(message="Missing error code")
