"""
Search router for search functionality
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.texts import get_text
from app.models import User

router = Router()

@router.message(Command("search"))
async def search_handler(message: Message, user: User, language: str = "uz"):
    """Handle search command"""
    search_text = get_text("search_menu", language)
    await message.answer(search_text)
