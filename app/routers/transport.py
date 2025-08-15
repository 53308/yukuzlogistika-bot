"""
Transport router for transport listings
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.texts import get_text
from app.models import User

router = Router()

@router.message(Command("transport"))
async def transport_handler(message: Message, user: User, language: str = "uz"):
    """Handle transport command"""
    transport_text = get_text("transport_menu", language)
    await message.answer(transport_text)
