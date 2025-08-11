"""
Main application entry point for the AI Legislation Tracking System
"""
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import time
from typing import Callable

from app.core.logging import setup_logging
from app.database.init import init_db
from app.routers import health, database
from app.core.logging import app_logger, log_request_info, log_response_info

# Create FastAPI application
app = FastAPI(
    title="AI Legislation Tracking System",
    description="API for tracking and analyzing AI legislation",
    version="0.1.0",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(database.router)

# Initialize database connections
init_db(app)

# Health check endpoints are now handled by the health router

# Request logging middleware
# @app.middleware("http")
# async def log_requests(request: Request, call_next: Callable) -> Response:
#     """
#     Middleware to log request and response information
    
#     Args:
#         request: The incoming request
#         call_next: The next middleware or route handler
        
#     Returns:
#         Response: The response from the next handler
#     """
#     # Log request
#     request_id = str(time.time())
#     request_info = {
#         "id": request_id,
#         "method": request.method,
#         "url": str(request.url),
#         "client": request.client.host if request.client else "unknown"
#     }
#     # log_request_info(app_logger, request_info)
    
#     # Process request
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
    
#     # Log response
#     response.headers["X-Process-Time"] = str(process_time)
#     # app_logger.info(f"Request {request_id} processed in {process_time:.4f} seconds")
    
#     return response
