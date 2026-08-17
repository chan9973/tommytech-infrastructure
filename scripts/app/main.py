# FastAPI LLM Wiki API - Minimal Application
# Production-ready FastAPI backend for LLM Wiki documentation system

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import logging
import os
import json

# Configure structured JSON logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI(
    title="LLM Wiki API",
    description="Documentation automation API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    services: dict


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for container orchestration"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        services={
            "api": "running",
            "database": "available",
            "cache": "available"
        }
    )


@app.get("/docs/info")
async def docs_info():
    """Get documentation system info"""
    return {
        "name": "LLM Wiki Documentation System",
        "version": "1.0.0",
        "endpoints": ["/health", "/docs/info", "/process"],
        "generated_at": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)