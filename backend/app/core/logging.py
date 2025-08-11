"""
Logging configuration for the application
"""
import logging
import sys
from typing import Dict, Any, Optional

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO


def setup_logging(name: str = "app", level: Optional[int] = None) -> logging.Logger:
    """
    Configure and return a logger with the specified name and level
    
    Args:
        name: Logger name
        level: Logging level (defaults to LOG_LEVEL)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set level from parameter or default
    logger.setLevel(level if level is not None else LOG_LEVEL)
    
    # Create console handler if not already added
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)
    
    return logger


def log_request_info(logger: logging.Logger, request_data: Dict[str, Any]) -> None:
    """
    Log request information
    
    Args:
        logger: Logger instance
        request_data: Request data to log
    """
    logger.info(f"Request received: {request_data}")


def log_response_info(logger: logging.Logger, status_code: int, response_data: Dict[str, Any]) -> None:
    """
    Log response information
    
    Args:
        logger: Logger instance
        status_code: HTTP status code
        response_data: Response data to log
    """
    logger.info(f"Response sent: status_code={status_code}, data={response_data}")


# Create default application logger
app_logger = setup_logging()
