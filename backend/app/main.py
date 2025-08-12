"""
Main application entry point for the AI Legislation Tracking System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.vector import db_manager
from app.routers import health, document, graph

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
app.include_router(document.router)
app.include_router(graph.router)
