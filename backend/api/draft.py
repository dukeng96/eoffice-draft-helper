"""Draft endpoints for document generation and refinement."""

import json
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse

from models.draft import GenerateRequest, RefineRequest
from services.llm_service import llm_service
from services.session_store import session_store
from prompts import build_generate_prompt, build_refine_prompt

router = APIRouter()


async def stream_generate_events(
    request: GenerateRequest,
    session_id: str
) -> AsyncGenerator[dict, None]:
    """Generate SSE events for draft generation."""
    draft_content = ""

    try:
        messages = build_generate_prompt(file_content=request.file_content)

        async for chunk in llm_service.stream_chat(messages):
            draft_content += chunk
            yield {
                "event": "chunk",
                "data": json.dumps({"content": chunk, "session_id": session_id})
            }

        # Store completed draft
        session_store.update_draft(session_id, draft_content)

        yield {
            "event": "done",
            "data": json.dumps({"status": "completed", "session_id": session_id})
        }

    except Exception as e:
        yield {
            "event": "error",
            "data": json.dumps({"error": str(e), "code": "LLM_ERROR"})
        }


async def stream_refine_events(
    session_id: str,
    instruction: str,
    current_draft: str
) -> AsyncGenerator[dict, None]:
    """Generate SSE events for draft refinement."""
    draft_content = ""

    try:
        messages = build_refine_prompt(
            current_draft=current_draft,
            instruction=instruction
        )

        async for chunk in llm_service.stream_chat(messages):
            draft_content += chunk
            yield {
                "event": "chunk",
                "data": json.dumps({"content": chunk, "session_id": session_id})
            }

        # Store updated draft
        session_store.update_draft(session_id, draft_content)

        yield {
            "event": "done",
            "data": json.dumps({"status": "completed", "session_id": session_id})
        }

    except Exception as e:
        yield {
            "event": "error",
            "data": json.dumps({"error": str(e), "code": "LLM_ERROR"})
        }


@router.post("/generate")
async def generate_draft(request: GenerateRequest):
    """
    Generate draft document from file content.

    Returns SSE stream with session_id for subsequent refine calls.
    """
    session_id = session_store.create_session(request.file_content)
    return EventSourceResponse(stream_generate_events(request, session_id))


@router.post("/refine")
async def refine_draft(request: RefineRequest):
    """
    Refine existing draft based on user instruction.

    Requires session_id from previous generate call.
    """
    session = session_store.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired")

    if not session["current_draft"]:
        raise HTTPException(status_code=400, detail="No draft found. Call /generate first.")

    return EventSourceResponse(
        stream_refine_events(
            session_id=request.session_id,
            instruction=request.instruction,
            current_draft=session["current_draft"]
        )
    )
