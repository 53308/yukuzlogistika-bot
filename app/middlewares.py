import time
import logging
from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import User

logger = logging.getLogger(__name__)

class ThrottleMiddleware(BaseMiddleware):
    def __init__(self, rate_seconds: int = 5):
        super().__init__()
        self.rate = rate_seconds
        self.bucket: dict[int, float] = {}

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]):
        if isinstance(event, (Message, CallbackQuery)) and event.from_user:
            now = time.time()
            last = self.bucket.get(event.from_user.id, 0)
            if now - last < self.rate:
                return
            self.bucket[event.from_user.id] = now
        return await handler(event, data)

class LoggingMiddleware(BaseMiddleware):
    """Middleware for logging user interactions"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, (Message, CallbackQuery)) and event.from_user:
            user = event.from_user
            if isinstance(event, Message):
                logger.info(f"Message from {user.id} (@{user.username or 'None'}): {event.text}")
            elif isinstance(event, CallbackQuery):
                logger.info(f"Callback from {user.id} (@{user.username or 'None'}): {event.data}")
        
        return await handler(event, data)

class DatabaseMiddleware(BaseMiddleware):
    """Middleware for database session and user management"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, (Message, CallbackQuery)) and event.from_user:
            session = await get_session()
            try:
                # Get or create user
                user = await self._get_or_create_user(session, event.from_user)
                
                # Add to data
                data["session"] = session
                data["user"] = user
                data["language"] = user.language if user else "uz"
                
                return await handler(event, data)
            except Exception as e:
                await session.rollback()
                logger.error(f"Database error in middleware: {e}")
                raise
            finally:
                await session.close()
        
        return await handler(event, data)
    
    async def _get_or_create_user(self, session: AsyncSession, tg_user) -> User:
        """Get existing user or create new one"""
        from sqlalchemy import select
        
        # Try to get existing user
        result = await session.execute(select(User).where(User.id == tg_user.id))
        user = result.scalar_one_or_none()
        
        if not user:
            # Create new user
            user = User(
                id=tg_user.id,
                username=tg_user.username,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                language="uz"
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        
        return user
