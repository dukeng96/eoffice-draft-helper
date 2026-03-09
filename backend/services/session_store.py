"""Redis-based session store for draft management."""

import json
import uuid
from typing import Optional

import redis

from config import settings


class SessionStore:
    """Redis-backed store for draft sessions."""

    def __init__(self):
        self._redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self._ttl_seconds = settings.SESSION_TTL_HOURS * 3600

    def _key(self, session_id: str) -> str:
        """Generate Redis key for session."""
        return f"draft:session:{session_id}"

    def create_session(self, file_content: str) -> str:
        """Create new session, return session_id."""
        session_id = str(uuid.uuid4())[:8]
        data = {
            "file_content": file_content,
            "current_draft": "",
        }
        self._redis.setex(
            self._key(session_id),
            self._ttl_seconds,
            json.dumps(data)
        )
        return session_id

    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session by ID, return None if not found or expired."""
        data = self._redis.get(self._key(session_id))
        if not data:
            return None
        return json.loads(data)

    def update_draft(self, session_id: str, draft: str) -> bool:
        """Update current draft for session."""
        key = self._key(session_id)
        data = self._redis.get(key)
        if not data:
            return False

        session = json.loads(data)
        session["current_draft"] = draft

        # Update with remaining TTL
        ttl = self._redis.ttl(key)
        if ttl > 0:
            self._redis.setex(key, ttl, json.dumps(session))
        else:
            self._redis.setex(key, self._ttl_seconds, json.dumps(session))

        return True


# Global instance
session_store = SessionStore()
