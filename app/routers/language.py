"""
Language router for language selection
"""
from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def language_handler(message: Message):
    """Handle language messages"""
    await message.answer("Language selection coming soon...")
