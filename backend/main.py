"""FastAPI main application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings, Settings

# Validate configuration on startup
Settings.validate()

app = FastAPI(
    title="eOffice Soạn Thảo AI API",
    description="AI service for Vietnamese document drafting",
    version="1.0.0"
)

# CORS middleware for DAS integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "eOffice Soạn Thảo AI",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "llm_configured": bool(settings.VNPT_API_KEY),
        "model": settings.VNPT_MODEL
    }


# Include draft router
from api.draft import router as draft_router
app.include_router(draft_router, prefix="/draft", tags=["draft"])
