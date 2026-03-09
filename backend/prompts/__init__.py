"""Prompts package."""

from .draft_prompts import (
    SYSTEM_PROMPT_GENERATE,
    SYSTEM_PROMPT_REFINE,
    FEWSHOT_SAMPLE_DEFAULT,
    build_generate_prompt,
    build_refine_prompt,
)

__all__ = [
    "SYSTEM_PROMPT_GENERATE",
    "SYSTEM_PROMPT_REFINE",
    "FEWSHOT_SAMPLE_DEFAULT",
    "build_generate_prompt",
    "build_refine_prompt",
]
