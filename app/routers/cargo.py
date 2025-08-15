"""
Cargo router for cargo listings
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.texts import get_text
from app.models import User

router = Router()

@router.message(Command("cargo"))
async def cargo_handler(message: Message, user: User, language: str = "uz"):
    """Handle cargo command"""
    cargo_text = get_text("cargo_menu", language)
    await message.answer(cargo_text)
