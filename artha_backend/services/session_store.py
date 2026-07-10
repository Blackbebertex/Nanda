"""Session store — in-memory with optional Redis backend."""
import json
import os
from typing import Any, Dict, List, Optional

_histories: Dict[str, List[Dict[str, str]]] = {}
_languages: Dict[str, str] = {}
_customers: Dict[str, str] = {}
_redis = None


def _get_redis():
    global _redis
    if _redis is not None:
        return _redis
    url = os.environ.get("REDIS_URL")
    if not url:
        return None
    try:
        import redis
        _redis = redis.from_url(url, decode_responses=True)
        return _redis
    except Exception:
        return None


def add_session(session_id: str, language: str, customer_id: str) -> None:
    if len(_histories) >= 100:
        oldest = next(iter(_histories))
        _histories.pop(oldest, None)
        _languages.pop(oldest, None)
        _customers.pop(oldest, None)
    _histories[session_id] = []
    _languages[session_id] = language
    _customers[session_id] = customer_id
    r = _get_redis()
    if r:
        try:
            r.set(f"session:lang:{session_id}", language)
            r.set(f"session:hist:{session_id}", "[]")
            r.set(f"session:cust:{session_id}", customer_id)
        except Exception:
            pass


def validate_session(session_id: str, customer_id: str) -> bool:
    stored = _customers.get(session_id)
    if stored:
        return stored == customer_id
    r = _get_redis()
    if r:
        try:
            stored = r.get(f"session:cust:{session_id}")
            if stored:
                return stored == customer_id
        except Exception:
            pass
    return False


def get_history(session_id: str) -> List[Dict[str, str]]:
    r = _get_redis()
    if r:
        try:
            raw = r.get(f"session:hist:{session_id}")
            if raw:
                return json.loads(raw)
        except Exception:
            pass
    return _histories.get(session_id, [])


def get_language(session_id: str) -> str:
    r = _get_redis()
    if r:
        try:
            lang = r.get(f"session:lang:{session_id}")
            if lang:
                return lang
        except Exception:
            pass
    return _languages.get(session_id, "en")


def append_turn(session_id: str, user: str, bot: str, language: Optional[str] = None) -> None:
    if session_id not in _histories:
        return
    _histories[session_id].append({"user": user, "bot": bot})
    if len(_histories[session_id]) > 8:
        _histories[session_id] = _histories[session_id][-8:]
    r = _get_redis()
    if r:
        try:
            r.set(f"session:hist:{session_id}", json.dumps(_histories[session_id]))
            if language:
                r.set(f"session:lang:{session_id}", language)
        except Exception:
            pass
