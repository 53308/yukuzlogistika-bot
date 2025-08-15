"""
Start router for initial bot interactions
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.texts import get_text
from app.keyboards import get_main_menu, get_button_type, get_language_menu, get_quick_search_menu
from app.models import User

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, language: str = "uz"):
    """Handle /start command"""
    welcome_text = get_text("start_welcome", language)
    menu = get_main_menu(language)
    await message.answer(welcome_text, reply_markup=menu)

@router.message(Command("help"))
async def help_handler(message: Message, language: str = "uz"):
    """Handle /help command"""
    help_text = get_text("help_text", language)
    await message.answer(help_text)

@router.message()
async def main_menu_handler(message: Message, language: str = "uz"):
    """Handle main menu button presses in any language"""
    if not message.text:
        return
        
    button_type = get_button_type(message.text)
    
    if button_type == "help":
        help_text = get_text("help_text", language)
        await message.answer(help_text)
    elif button_type == "quick_search":
        search_text = get_text("quick_search_menu", language)
        search_kb = get_quick_search_menu(language)
        await message.answer(search_text, reply_markup=search_kb)
    elif button_type == "my_listings":
        listings_text = get_text("my_listings", language)
        await message.answer(listings_text)
    elif button_type == "add_listing":
        add_text = get_text("add_listing", language)
        await message.answer(add_text)
    elif button_type == "settings":
        settings_text = get_text("settings_menu", language)
        language_kb = get_language_menu()
        await message.answer(settings_text, reply_markup=language_kb)

@router.callback_query(F.data.startswith("lang:"))
async def language_callback_handler(callback: CallbackQuery, session: AsyncSession, user: User):
    """Handle language selection"""
    language_code = callback.data.split(":")[1]
    
    # Update user language in database
    user.language = language_code
    await session.commit()
    
    # Get new menu with updated language
    new_menu = get_main_menu(language_code)
    
    # Send confirmation message
    confirmation_text = get_text("language_selected", language_code)
    await callback.message.answer(confirmation_text, reply_markup=new_menu)
    await callback.answer()

@router.callback_query(F.data.startswith("search:"))
async def search_callback_handler(callback: CallbackQuery, language: str = "uz"):
    """Handle search menu actions"""
    action = callback.data.split(":")[1]
    
    if action == "cargo":
        cargo_text = get_text("cargo_search_title", language)
        await callback.message.answer(cargo_text)
    elif action == "transport":
        transport_text = get_text("transport_search_title", language)
        await callback.message.answer(transport_text)
    elif action == "back":
        main_menu = get_main_menu(language)
        back_text = get_text("main_menu", language)
        await callback.message.answer(back_text, reply_markup=main_menu)
    
    await callback.answer()
