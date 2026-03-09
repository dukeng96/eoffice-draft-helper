"""VNPT LLM service using OpenAI-compatible client."""

from typing import AsyncGenerator, List, Dict, Any, Optional
from openai import AsyncOpenAI
from config import settings


class LLMService:
    """Service for interacting with VNPT LLM API."""

    def __init__(self):
        """Initialize OpenAI client with VNPT configuration."""
        self.client = AsyncOpenAI(
            api_key=settings.VNPT_API_KEY,
            base_url=settings.VNPT_BASE_URL
        )
        self.model = settings.VNPT_MODEL

    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat completion from VNPT LLM.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate

        Yields:
            Content chunks from the LLM response
        """
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            raise RuntimeError(f"LLM streaming error: {str(e)}")

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Non-streaming chat completion (fallback).

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate

        Returns:
            Complete LLM response content
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )

            return response.choices[0].message.content

        except Exception as e:
            raise RuntimeError(f"LLM error: {str(e)}")


# Singleton instance
llm_service = LLMService()
