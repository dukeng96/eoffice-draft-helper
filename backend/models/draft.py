"""Pydantic models for draft API."""

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    """Request model for /draft/generate endpoint."""

    file_content: str = Field(..., description="Extracted text from PDF/DOCX", min_length=1)


class RefineRequest(BaseModel):
    """Request model for /draft/refine endpoint."""

    session_id: str = Field(..., description="Session ID from generate response")
    instruction: str = Field(..., description="Refinement instruction", min_length=1)
