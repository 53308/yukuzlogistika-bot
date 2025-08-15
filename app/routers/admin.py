"""
Admin router for bot administration
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.texts import get_text
from app.models import User

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message, user: User, language: str = "uz"):
    """Admin panel access"""
    admin_text = get_text("admin_panel", language)
    await message.answer(admin_text)
