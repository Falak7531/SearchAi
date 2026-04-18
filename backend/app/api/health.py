"""
api/health.py - Health check endpoint.
Used by load balancers and monitoring tools to verify service status.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/")
async def health_check():
    """Returns service health status and current timestamp."""
    return {
        "status": "healthy",
        "service": "AI E-Commerce Search API",
        "timestamp": datetime.utcnow().isoformat(),
    }
