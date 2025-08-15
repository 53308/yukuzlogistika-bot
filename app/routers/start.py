"""
Start router for initial bot interactions
"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from app.texts import get_text
from app.keyboards import MAIN_MENU

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, language: str = "uz"):
    """Handle /start command"""
    welcome_text = get_text("start_welcome", language)
    await message.answer(welcome_text, reply_markup=MAIN_MENU)

@router.message(Command("help"))
async def help_handler(message: Message, language: str = "uz"):
    """Handle /help command"""
    help_text = get_text("help_text", language)
    await message.answer(help_text)

@router.message(F.text == "❓ Помощь")
async def help_button_handler(message: Message, language: str = "ru"):
    """Handle help button press"""
    help_text = get_text("help_text", language)
    await message.answer(help_text)

@router.message(F.text == "🗣 Тезkor Qidiruv")
async def quick_search_handler(message: Message, language: str = "uz"):
    """Handle quick search button"""
    search_text = get_text("quick_search_menu", language)
    await message.answer(search_text)

@router.message(F.text == "📋 Mening e'lonlarim")
async def my_listings_handler(message: Message, language: str = "uz"):
    """Handle my listings button"""
    listings_text = get_text("my_listings", language)
    await message.answer(listings_text)

@router.message(F.text == "➕ E'lon qo'shish")
async def add_listing_handler(message: Message, language: str = "uz"):
    """Handle add listing button"""
    add_text = get_text("add_listing", language)
    await message.answer(add_text)

@router.message(F.text == "⚙️ Sozlamalar")
async def settings_handler(message: Message, language: str = "uz"):
    """Handle settings button"""
    settings_text = get_text("settings_menu", language)
    await message.answer(settings_text)
