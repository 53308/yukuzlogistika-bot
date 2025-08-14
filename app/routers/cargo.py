"""
Cargo router for cargo-related functionality
"""
from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def cargo_handler(message: Message):
    """Handle cargo messages"""
    await message.answer("Cargo functionality coming soon...")
