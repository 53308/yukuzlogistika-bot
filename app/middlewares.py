import time
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

class ThrottleMiddleware(BaseMiddleware):
    def __init__(self, rate_seconds: int = 5):
        super().__init__()
        self.rate = rate_seconds
        self.bucket: dict[int, float] = {}

    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]):
        now = time.time()
        last = self.bucket.get(event.from_user.id, 0)
        if now - last < self.rate:
            return
        self.bucket[event.from_user.id] = now
        return await handler(event, data)
