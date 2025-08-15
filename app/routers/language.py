"""
Language router for language switching
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.texts import get_text
from app.keyboards import get_language_menu, get_main_menu
from app.models import User

router = Router()

@router.message(Command("language"))
async def language_handler(message: Message, user: User, language: str = "uz"):
    """Handle language command"""
    language_text = get_text("language_menu", language)
    language_kb = get_language_menu()
    await message.answer(language_text, reply_markup=language_kb)

@router.callback_query(F.data.startswith("set_lang:"))
async def set_language_handler(callback: CallbackQuery, session: AsyncSession, user: User):
    """Handle language selection"""
    if not callback.data:
        return
        
    lang_code = callback.data.split(":")[1]
    
    # Update user language
    user.language = lang_code
    session.add(user)
    await session.commit()
    
    # Send confirmation
    success_text = get_text("language_set", lang_code)
    main_menu = get_main_menu(lang_code)
    
    await callback.message.answer(success_text, reply_markup=main_menu)
    await callback.answer()
