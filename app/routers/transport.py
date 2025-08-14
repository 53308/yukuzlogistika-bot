"""
Transport router for transport-related functionality
"""
from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def transport_handler(message: Message):
    """Handle transport messages"""
    await message.answer("Transport functionality coming soon...")
