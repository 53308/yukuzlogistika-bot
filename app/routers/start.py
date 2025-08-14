"""
Start router for initial bot interactions
"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.texts import get_text

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, language: str = "uz"):
    """Handle /start command"""
    welcome_text = get_text("start_welcome", language)
    await message.answer(welcome_text)
