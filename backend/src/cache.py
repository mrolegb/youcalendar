import hashlib
import os
import json
from typing import Any
from redis import Redis


class Cache:
    cache = None

    def __init__(self, cache_url: str, cache_port: int):
        self.cache = Redis(
            host=cache_url,
            port=cache_port,
        )

    def write(self, request: dict[str, Any], response: str) -> bool | None:
        key = self.encrypt(request)
        if self.cache:
            return self.cache.set(
                key,
                response,
                ex=int(os.environ["CACHE_LIFE"]) * 24 * 60 * 60,
            )

    def read(self, request: dict[str, Any]) -> bytes | None:
        key = self.encrypt(request)
        if self.cache:
            return self.cache.get(key)
        return None

    def encrypt(self, request: dict[str, Any]) -> str:
        s = json.dumps(request)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()
