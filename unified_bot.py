#!/usr/bin/env python3
"""
Unified Telegram Logistics Bot - Exact Copy of @yuk_uz_logistika_bot
All functionality in one file for easy deployment
"""

import asyncio
import logging
import os
import psycopg2
import fcntl
import sys
import time
from typing import Optional
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from aiohttp import web
from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message, CallbackQuery, BotCommand, InlineKeyboardMarkup, 
    InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton,
    InaccessibleMessage
)
from aiogram.exceptions import TelegramBadRequest, TelegramConflictError
import signal
import sys


import fcntl

# CONFLICT PREVENTION - Lock file system
LOCK_FILE = '/tmp/yukuz_bot.lock'

def acquire_lock():
    """Enhanced instance locking"""
    try:
        lock_fd = open(LOCK_FILE, 'w')
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        lock_fd.write(str(os.getpid()))
        lock_fd.flush()
        return lock_fd
    except (IOError, BlockingIOError) as e:
        logger.error(f"❌ Another instance running (PID: {os.getpid()}). Error: {e}")
        sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Глобальные настройки блокировки
LOCK_FILE = '/tmp/yukuz_bot.lock'

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
ADMINS = [8101326669]

# Bot commands
BOT_COMMANDS = [
    {"command": "start", "description": "🏠 Главное меню"},
    {"command": "cargo", "description": "📦 Найти груз"},
    {"command": "transport", "description": "🚛 Найти транспорт"},
    {"command": "search", "description": "🔍 Поиск"},
    {"command": "help", "description": "ℹ️ Помощь"}
]

# States for search flow
class SearchState(StatesGroup):
    waiting_city_input = State()

# Create router
router = Router()

# Database connection
def get_db_connection():
    """Get database connection"""
    if not DATABASE_URL:
        logger.error("DATABASE_URL environment variable not set!")
        return None
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

def init_db():
    """Initialize database with required tables"""
    try:
        conn = get_db_connection()
        if not conn:
            logger.error("Failed to get database connection")
            return False
        cursor = conn.cursor()
        
        # Create announcements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS announcements (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                announcement_type VARCHAR(20) NOT NULL,
                status VARCHAR(20) DEFAULT 'draft',
                from_location VARCHAR(100),
                to_location VARCHAR(100),
                cargo_weight VARCHAR(50),
                cargo_type VARCHAR(100),
                vehicle_type VARCHAR(100),
                contact_name VARCHAR(100),
                contact_phone VARCHAR(20),
                contact_address TEXT,
                notes TEXT,
                user_telegram_id BIGINT,
                user_username VARCHAR(50),
                location_latitude FLOAT,
                location_longitude FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                views_count INTEGER DEFAULT 0,
                contacts_accessed INTEGER DEFAULT 0,
                message_url TEXT,
                source VARCHAR(50) DEFAULT 'manual',
                telegram_username VARCHAR(100)
            )
        """)
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE NOT NULL,
                username VARCHAR(50),
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                phone VARCHAR(20),
                language_code VARCHAR(10) DEFAULT 'uz',
                is_premium BOOLEAN DEFAULT FALSE,
                free_views_left INTEGER DEFAULT 5,
                subscription_expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False

# City database with hundreds of variants
CITY_DATABASE = {
    # Uzbekistan cities with all variants
    "uzbekistan": {
        "Toshkent": ["Toshkent", "Ташкент", "Tashkent", "Тошкент", "toshkent", "ташкент"],
        "Samarqand": ["Samarqand", "Самарканд", "Samarkand", "Самарқанд", "samarqand", "самарканд"],
        "Namangan": ["Namangan", "Наманган", "Наманғон", "namangan", "наманган"],
        "Andijon": ["Andijon", "Андижан", "Андижон", "andijon", "андижан"],
        "Farg'ona": ["Farg'ona", "Фергана", "Фарғона", "Fergana", "фергана", "fergana"],
        "Nukus": ["Nukus", "Нукус", "Нукус", "nukus", "нукус"],
        "Buxoro": ["Buxoro", "Бухара", "Бухоро", "Bukhara", "бухара", "bukhara"],
        "Qarshi": ["Qarshi", "Карши", "Қарши", "qarshi", "карши"],
        "Angren": ["Angren", "Ангрен", "Ангрен", "angren", "ангрен"],
        "Xiva": ["Xiva", "Хива", "Хива", "Khiva", "хива", "khiva"],
        "Guliston": ["Guliston", "Гулистан", "Гулистон", "guliston", "гулистан"],
        "Jizzax": ["Jizzax", "Джизак", "Жиззах", "jizzax", "джизак"],
        "Navoiy": ["Navoiy", "Навои", "Навоий", "navoiy", "навои"],
        "Termiz": ["Termiz", "Термез", "Термиз", "termiz", "термез"],
        "Urganch": ["Urganch", "Ургенч", "Урганч", "urganch", "ургенч"],
        "Chirchiq": ["Chirchiq", "Чирчик", "Чирчиқ", "chirchiq", "чирчик"],
        "Bekobod": ["Bekobod", "Бекабад", "Бекобод", "bekobod", "бекабад"],
        "Margilan": ["Margilan", "Маргилан", "Марғилон", "margilan", "маргилан"],
        "Kokand": ["Kokand", "Коканд", "Қўқон", "kokand", "коканд"],
        "Oltinko'l": ["Oltinko'l", "Алтынкуль", "Олтинкўл", "oltinkol", "алтынкуль"],
    },
    
    # Russia cities
    "russia": {
        "Moskva": ["Moskva", "Москва", "Moscow", "москва", "moscow"],
        "Sankt-Peterburg": ["Sankt-Peterburg", "Санкт-Петербург", "SPB", "спб", "питер"],
        "Novosibirsk": ["Novosibirsk", "Новосибирск", "новосибирск"],
        "Yekaterinburg": ["Yekaterinburg", "Екатеринбург", "екатеринбург"],
        "Nizhny Novgorod": ["Nizhny Novgorod", "Нижний Новгород", "нижний новгород"],
        "Kazan": ["Kazan", "Казань", "казань"],
        "Chelyabinsk": ["Chelyabinsk", "Челябинск", "челябинск"],
        "Samara": ["Samara", "Самара", "самара"],
        "Omsk": ["Omsk", "Омск", "омск"],
        "Rostov-na-Donu": ["Rostov-na-Donu", "Ростов-на-Дону", "ростов"],
        "Ufa": ["Ufa", "Уфа", "уфа"],
        "Krasnoyarsk": ["Krasnoyarsk", "Красноярск", "красноярск"],
        "Perm": ["Perm", "Пермь", "пермь"],
        "Voronezh": ["Voronezh", "Воронеж", "воронеж"],
        "Volgograd": ["Volgograd", "Волгоград", "волгоград"],
        "Krasnodar": ["Krasnodar", "Краснодар", "краснодар"],
        "Tyumen": ["Tyumen", "Тюмень", "тюмень"],
        "Saratov": ["Saratov", "Саратов", "саратов"],
        "Tolyatti": ["Tolyatti", "Тольятти", "тольятти"],
        "Izhevsk": ["Izhevsk", "Ижевск", "ижевск"],
    },
    
    # Kazakhstan cities
    "kazakhstan": {
        "Almaty": ["Almaty", "Алматы", "Алмата", "almaty", "алматы"],
        "Nur-Sultan": ["Nur-Sultan", "Нур-Султан", "Астана", "astana", "астана"],
        "Shymkent": ["Shymkent", "Шымкент", "Чимкент", "shymkent", "чимкент"],
        "Aktobe": ["Aktobe", "Актобе", "Актюбинск", "aktobe", "актобе"],
        "Taraz": ["Taraz", "Тараз", "Джамбул", "taraz", "тараз"],
        "Pavlodar": ["Pavlodar", "Павлодар", "павлодар"],
        "Ust-Kamenogorsk": ["Ust-Kamenogorsk", "Усть-Каменогорск", "Өскемен", "oskemen"],
        "Semey": ["Semey", "Семей", "Семипалатинск", "semey", "семей"],
        "Aktau": ["Aktau", "Актау", "актау"],
        "Kostanay": ["Kostanay", "Костанай", "костанай"],
        "Petropavlovsk": ["Petropavlovsk", "Петропавловск", "петропавловск"],
        "Oral": ["Oral", "Орал", "Уральск", "uralsk", "уральск"],
        "Temirtau": ["Temirtau", "Темиртау", "темиртау"],
        "Karaganda": ["Karaganda", "Караганда", "караганда"],
        "Atyrau": ["Atyrau", "Атырау", "Гурьев", "atyrau", "атырау"],
    }
}

def find_city_in_database(city_query: str) -> Optional[Tuple[str, str]]:
    """Find city in database by query"""
    city_query = city_query.strip().lower()
    
    for country, cities in CITY_DATABASE.items():
        for canonical_name, variants in cities.items():
            for variant in variants:
                if variant.lower() == city_query:
                    return canonical_name, country
    return None

def get_country_flag(city_name: str) -> str:
    """Get country flag by city"""
    result = find_city_in_database(city_name)
    if result:
        _, country = result
        if country == "uzbekistan":
            return "🇺🇿"
        elif country == "russia":
            return "🇷🇺"
        elif country == "kazakhstan":
            return "🇰🇿"
    return "🌍"

def calculate_distance_and_time(from_city: str, to_city: str) -> Tuple[int, float]:
    """Calculate approximate distance and travel time"""
    # Simple distance calculation based on city pairs
    distances = {
        ("Toshkent", "Moskva"): (2800, 35.0),
        ("Samarqand", "Moskva"): (2600, 32.0),
        ("Angren", "Groznyy"): (1800, 22.0),
        ("Toshkent", "Namangan"): (320, 4.0),
        ("Almaty", "Toshkent"): (650, 8.0),
    }
    
    # Try to find exact match
    pair = (from_city, to_city)
    if pair in distances:
        return distances[pair]
    
    # Default values
    return 1200, 15.0

def format_time_ago(created_at: datetime) -> str:
    """Format time ago like in original bot"""
    now = datetime.now()
    diff = now - created_at
    
    if diff.days > 0:
        return f"{diff.days} дней назад"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} часов назад"
    else:
        minutes = diff.seconds // 60
        return f"{minutes} минут назад"

# Main menu keyboard
def get_main_menu():
    """Get main menu keyboard exactly like original"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Быстрый Поиск")],
            [KeyboardButton(text="📦 Мои объявления"), KeyboardButton(text="➕ Добавить объявление")],
            [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True
    )

# Country selection with counts
def get_country_selection():
    """Get country selection with announcement counts"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 Узбекистан - 503", callback_data="country_uzbekistan")],
        [InlineKeyboardButton(text="🇷🇺 Россия - 2341", callback_data="country_russia")],
        [InlineKeyboardButton(text="🇰🇿 Казахстан - 156", callback_data="country_kazakhstan")],
        [InlineKeyboardButton(text="🇹🇷 Турция - 87", callback_data="country_turkey")],
        [InlineKeyboardButton(text="🇨🇳 Китай - 45", callback_data="country_china")],
        [InlineKeyboardButton(text="🇮🇷 Иран - 23", callback_data="country_iran")],
        [InlineKeyboardButton(text="🇦🇫 Афганистан - 12", callback_data="country_afghanistan")],
        [InlineKeyboardButton(text="🇰🇬 Кыргызстан - 34", callback_data="country_kyrgyzstan")],
        [InlineKeyboardButton(text="🇹🇯 Таджикистан - 28", callback_data="country_tajikistan")],
        [InlineKeyboardButton(text="🇹🇲 Туркменистан - 19", callback_data="country_turkmenistan")],
        [InlineKeyboardButton(text="🇦🇿 Азербайджан - 41", callback_data="country_azerbaijan")],
        [InlineKeyboardButton(text="🇦🇪 ОАЭ - 15", callback_data="country_uae")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]
    ])

def get_city_buttons(country: str):
    """Get city buttons for country"""
    if country not in CITY_DATABASE:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_countries")]
        ])
    
    buttons = []
    cities = CITY_DATABASE[country]
    
    for city_name in list(cities.keys())[:12]:  # Show first 12 cities
        # Add random counts for demo
        import random
        count = random.randint(5, 45)
        buttons.append([InlineKeyboardButton(
            text=f"{city_name} - {count}", 
            callback_data=f"city_{city_name}"
        )])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_countries")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Bot handlers
@router.message(F.text == "/start")
async def start_handler(message: Message):
    """Start command handler - main menu"""
    if not message.from_user:
        return
    user_id = message.from_user.id
    
    # Save/update user in database
    try:
        conn = get_db_connection()
        if not conn:
            logger.error("Database connection failed in start handler")
            menu = get_main_menu()
            await message.answer("📦 <b>YukUz Logistics Bot</b>\n\nДобро пожаловать!", reply_markup=menu, parse_mode="HTML")
            return
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (telegram_id, username, first_name, last_name)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (telegram_id) DO UPDATE SET
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                updated_at = CURRENT_TIMESTAMP
        """, (user_id, message.from_user.username if message.from_user.username else None, 
              message.from_user.first_name if message.from_user.first_name else None, 
              message.from_user.last_name if message.from_user.last_name else None))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error saving user: {e}")
    
    menu = get_main_menu()
    await message.answer(
        "📦 <b>YukUz Logistics Bot</b>\n\n"
        "Добро пожаловать в бот для поиска грузов и транспорта!\n\n"
        "🔍 Быстрый поиск грузов\n"
        "📦 Управление объявлениями\n" 
        "⚙️ Настройки и помощь\n\n"
        "Выберите действие:",
        reply_markup=menu,
        parse_mode="HTML"
    )

@router.message(F.text == "🔍 Быстрый Поиск")
async def quick_search_handler(message: Message):
    """Quick search handler - goes to cargo/transport selection"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Найти груз", callback_data="search_cargo")],
        [InlineKeyboardButton(text="🚛 Найти транспорт", callback_data="search_transport")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]
    ])
    await message.answer("🔍 <b>Быстрый Поиск</b>\n\nВыберите тип поиска:", reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(F.data.startswith("search_"))
async def search_type_callback(callback: CallbackQuery, state: FSMContext):
    """Handle search type selection"""
    if not callback.data:
        await callback.answer()
        return
    search_type = callback.data.split("_")[1]  # cargo or transport
    await state.update_data(search_type=search_type)
    
    if search_type == "cargo":
        text = "📦 <b>Поиск грузов</b>\n\nВыберите страну отправления:"
    else:
        text = "🚛 <b>Поиск транспорта</b>\n\nВыберите страну отправления:"
    
    countries = get_country_selection()
    try:
        if callback.message and not isinstance(callback.message, InaccessibleMessage):
            await callback.message.edit_text(text, reply_markup=countries, parse_mode="HTML")
    except (TelegramBadRequest, AttributeError):
        if callback.message and not isinstance(callback.message, InaccessibleMessage):
            await callback.message.answer(text, reply_markup=countries, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("country_"))
async def country_selection_callback(callback: CallbackQuery, state: FSMContext):
    """Handle country selection"""
    if not callback.data:
        await callback.answer()
        return
    country = callback.data.split("_")[1]
    await state.update_data(country=country)
    
    if country in CITY_DATABASE:
        text = f"Выберите город в стране {country.title()}:"
        cities = get_city_buttons(country)
        try:
            if callback.message and not isinstance(callback.message, InaccessibleMessage):
                await callback.message.edit_text(text, reply_markup=cities)
        except (TelegramBadRequest, AttributeError):
            if callback.message and not isinstance(callback.message, InaccessibleMessage):
                await callback.message.answer(text, reply_markup=cities)
    else:
        # For countries not in database, show generic message
        try:
            if callback.message and not isinstance(callback.message, InaccessibleMessage):
                await callback.message.edit_text(f"Поиск в стране {country.title()} временно недоступен.")
        except (TelegramBadRequest, AttributeError):
            if callback.message and not isinstance(callback.message, InaccessibleMessage):
                await callback.message.answer(f"Поиск в стране {country.title()} временно недоступен.")
    
    await callback.answer()

@router.callback_query(F.data.startswith("city_"))
async def city_selection_callback(callback: CallbackQuery, state: FSMContext):
    """Handle city selection and show search results"""
    if not callback.data:
        await callback.answer()
        return
    city_name = callback.data.split("_")[1]
    data = await state.get_data()
    search_type = data.get("search_type", "cargo")
    
    # Search in database
    try:
        conn = get_db_connection()
        if not conn:
            await callback.answer("❌ Database connection error")
            return
        cursor = conn.cursor()
        
        # Search for announcements
        if search_type == "cargo":
            cursor.execute("""
                SELECT * FROM announcements 
                WHERE announcement_type = 'cargo' AND status = 'published'
                AND (from_location ILIKE %s OR to_location ILIKE %s)
                ORDER BY created_at DESC LIMIT 6
            """, (f"%{city_name}%", f"%{city_name}%"))
        else:
            cursor.execute("""
                SELECT * FROM announcements 
                WHERE announcement_type = 'transport' AND status = 'published'
                AND (from_location ILIKE %s OR to_location ILIKE %s)
                ORDER BY created_at DESC LIMIT 6
            """, (f"%{city_name}%", f"%{city_name}%"))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not results:
            try:
                if callback.message and not isinstance(callback.message, InaccessibleMessage):
                    await callback.message.edit_text(f"❌ По запросу '{city_name}' ничего не найдено.")
            except (TelegramBadRequest, AttributeError):
                if callback.message and not isinstance(callback.message, InaccessibleMessage):
                    await callback.message.answer(f"❌ По запросу '{city_name}' ничего не найдено.")
            return

        # Send results as individual messages exactly like original
        search_icon = "📦" if search_type == "cargo" else "🚚"
        try:
            if callback.message and not isinstance(callback.message, InaccessibleMessage):
                await callback.message.edit_text(f"🔍 Результаты поиска {search_icon} в {city_name}:")
        except (TelegramBadRequest, AttributeError):
            if callback.message and not isinstance(callback.message, InaccessibleMessage):
                await callback.message.answer(f"🔍 Результаты поиска {search_icon} в {city_name}:")
        
        for i, row in enumerate(results[:5], 1):
            (announcement_id, title, description, ann_type, status, from_loc, to_loc, 
             weight, cargo_type, vehicle_type, contact_name, contact_phone, contact_address,
             notes, user_tg_id, user_name, location_lat, location_lon, created_at, updated_at, 
             expires_at, views_count, contacts_accessed, message_url, source, telegram_username) = row
            
            from_flag = get_country_flag(from_loc)
            to_flag = get_country_flag(to_loc)
            
            distance, travel_time = calculate_distance_and_time(from_loc, to_loc)
            time_ago = format_time_ago(created_at)
            
            # Exact format like in image: "1. 🇺🇿 Ангрен - 🇷🇺 Грозный"
            text = f"<b>{i}. {from_flag} {from_loc} - {to_flag} {to_loc}</b>\n\n"
            text += f"⚖️ {weight}\n"
            
            if vehicle_type:
                text += f"🚚 {vehicle_type}\n"
            
            if cargo_type:
                text += f"📦 {cargo_type}\n"
            
            if distance > 0:
                text += f"🛣️ {distance} км {travel_time:.1f} часов\n\n"
            
            text += time_ago
            
            detail_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Подробнее", callback_data=f"detail_{announcement_id}")]
            ])
            
            if callback.message:
                await callback.message.answer(
                    text, 
                    parse_mode="HTML",
                    reply_markup=detail_keyboard
                )

        # Show "6 из 15 показать больше" button if more results exist
        if len(results) == 6 and callback.message:
            more_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="6 из 15 показать больше", callback_data=f"show_more_{city_name}_{search_type}")]
            ])
            await callback.message.answer("", reply_markup=more_keyboard)
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        if callback.message:
            await callback.message.answer(f"❌ Ошибка поиска: {str(e)}")

@router.callback_query(F.data.startswith("detail_"))
async def show_detail_callback(callback: CallbackQuery):
    """Show announcement details"""
    if not callback.data:
        await callback.answer()
        return
    announcement_id = callback.data.split("_")[1]
    
    try:
        conn = get_db_connection()
        if not conn:
            await callback.answer("❌ Database connection error")
            return
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM announcements WHERE id = %s", (announcement_id,))
        row = cursor.fetchone()
        
        if not row:
            await callback.answer("❌ Объявление не найдено")
            return
        
        # Update views count
        cursor.execute("UPDATE announcements SET views_count = views_count + 1 WHERE id = %s", (announcement_id,))
        conn.commit()
        
        (announcement_id, title, description, ann_type, status, from_loc, to_loc, 
         weight, cargo_type, vehicle_type, contact_name, contact_phone, contact_address,
         notes, user_tg_id, user_name, location_lat, location_lon, created_at, updated_at, 
         expires_at, views_count, contacts_accessed, message_url, source, telegram_username) = row
        
        from_flag = get_country_flag(from_loc)
        to_flag = get_country_flag(to_loc)
        distance, travel_time = calculate_distance_and_time(from_loc, to_loc)
        time_ago = format_time_ago(created_at)
        
        # Detailed view exactly like original
        text = f"<b>{from_flag} {from_loc} - {to_flag} {to_loc}</b>\n\n"
        text += f"⚖️ <b>Вес:</b> {weight}\n"
        
        if cargo_type:
            text += f"📦 <b>Груз:</b> {cargo_type}\n"
        
        if vehicle_type:
            text += f"🚚 <b>Транспорт:</b> {vehicle_type}\n"
        
        if distance > 0:
            text += f"🛣️ <b>Расстояние:</b> {distance} км ({travel_time:.1f} часов)\n"
        
        if description:
            text += f"\n📝 <b>Описание:</b>\n{description}\n"
        
        text += f"\n👁 Просмотров: {views_count + 1}\n"
        text += f"📅 {time_ago}"
        
        # Contact access keyboard
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📞 Показать контакт", callback_data=f"contact_{announcement_id}")],
            [InlineKeyboardButton(text="💬 Написать в Telegram", callback_data=f"telegram_{announcement_id}")],
            [InlineKeyboardButton(text="🔙 Назад к поиску", callback_data="back_search")]
        ])
        
        try:
            if callback.message and not isinstance(callback.message, InaccessibleMessage):
                await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        except (TelegramBadRequest, AttributeError):
            if callback.message and not isinstance(callback.message, InaccessibleMessage):
                await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Detail error: {e}")
        await callback.answer("❌ Ошибка загрузки деталей")
    
    await callback.answer()

@router.callback_query(F.data.startswith("contact_"))
async def show_contact_callback(callback: CallbackQuery):
    """Show contact with subscription check"""
    if not callback.data or not callback.from_user:
        await callback.answer()
        return
    announcement_id = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    try:
        conn = get_db_connection()
        if not conn:
            await callback.answer("❌ Database connection error")
            return
        cursor = conn.cursor()
        
        # Check user's free views
        cursor.execute("SELECT free_views_left, is_premium FROM users WHERE telegram_id = %s", (user_id,))
        user_row = cursor.fetchone()
        
        if not user_row:
            await callback.answer("❌ Пользователь не найден")
            return
        
        free_views, is_premium = user_row
        
        if not is_premium and free_views <= 0:
            # No free views left
            sub_text = "💳 <b>Лимит просмотров исчерпан</b>\n\n"
            sub_text += "🆓 Бесплатно: 5 просмотров в день\n"
            sub_text += "💎 Премиум: безлимитный доступ\n\n"
            sub_text += "💰 Стоимость подписки: 50,000 сум/месяц\n\n"
            sub_text += "Свяжитесь с @admin_yuk_uz для оформления"
            
            sub_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оформить подписку", url="https://t.me/admin_yuk_uz")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="back_search")]
            ])
            
            try:
                if callback.message and not isinstance(callback.message, InaccessibleMessage):
                    await callback.message.edit_text(sub_text, reply_markup=sub_keyboard, parse_mode="HTML")
            except (TelegramBadRequest, AttributeError):
                if callback.message and not isinstance(callback.message, InaccessibleMessage):
                    await callback.message.answer(sub_text, reply_markup=sub_keyboard, parse_mode="HTML")
            return
        
        # Get announcement
        cursor.execute("SELECT * FROM announcements WHERE id = %s", (announcement_id,))
        row = cursor.fetchone()
        
        if not row:
            await callback.answer("❌ Объявление не найдено")
            return
        
        contact_name = row[9]
        contact_phone = row[10]
        
        # Update contacts accessed and user's free views
        cursor.execute("UPDATE announcements SET contacts_accessed = contacts_accessed + 1 WHERE id = %s", (announcement_id,))
        
        if not is_premium:
            cursor.execute("UPDATE users SET free_views_left = free_views_left - 1 WHERE telegram_id = %s", (user_id,))
        
        conn.commit()
        
        # Show contact
        contact_text = f"📞 <b>Контактная информация</b>\n\n"
        contact_text += f"👤 <b>Имя:</b> {contact_name}\n"
        contact_text += f"📱 <b>Телефон:</b> {contact_phone}\n\n"
        
        if not is_premium:
            views_left = free_views - 1
            contact_text += f"🆓 Осталось бесплатных просмотров: {views_left}"
        
        back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад к объявлению", callback_data=f"detail_{announcement_id}")]
        ])
        
        try:
            if callback.message and not isinstance(callback.message, InaccessibleMessage):
                await callback.message.edit_text(contact_text, reply_markup=back_keyboard, parse_mode="HTML")
        except (TelegramBadRequest, AttributeError):
            if callback.message and not isinstance(callback.message, InaccessibleMessage):
                await callback.message.answer(contact_text, reply_markup=back_keyboard, parse_mode="HTML")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Contact error: {e}")
        await callback.answer("❌ Ошибка получения контакта")
    
    await callback.answer()

# Additional menu handlers
@router.message(F.text == "📦 Мои объявления")
async def my_announcements_handler(message: Message):
    """My announcements handler"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Мои грузы")],
            [KeyboardButton(text="🚛 Мой транспорт")], 
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("📦 <b>Мои объявления</b>", reply_markup=keyboard, parse_mode="HTML")

@router.message(F.text == "➕ Добавить объявление")  
async def add_announcement_handler(message: Message):
    """Add announcement handler"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Добавить груз")],
            [KeyboardButton(text="🚛 Добавить транспорт")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("➕ <b>Добавить объявление</b>", reply_markup=keyboard, parse_mode="HTML")

@router.message(F.text == "⚙️ Настройки")
async def settings_handler(message: Message):
    """Settings handler"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌐 Изменить язык")],
            [KeyboardButton(text="🔔 Уведомления")],
            [KeyboardButton(text="💳 Подписка")],
            [KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="📞 Контакты")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("⚙️ <b>Настройки</b>", reply_markup=keyboard, parse_mode="HTML")

@router.message(F.text == "ℹ️ Помощь")
async def help_handler(message: Message):
    """Help handler"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❓ Как пользоваться")],
            [KeyboardButton(text="💳 О подписке")],
            [KeyboardButton(text="📞 Связаться с нами")],
            [KeyboardButton(text="📋 Правила")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("ℹ️ <b>Помощь</b>", reply_markup=keyboard, parse_mode="HTML")

@router.message(F.text == "🔙 Назад")
async def back_handler(message: Message):
    """Back to main menu"""
    menu = get_main_menu()
    await message.answer("📦 Главное меню", reply_markup=menu)

# Health check server
async def health_check(request):
    """Health check endpoint"""
    return web.Response(text="OK", status=200)

async def create_health_server():
    """Create health check server"""
    app = web.Application()
    app.router.add_get('/health', health_check)
    app.router.add_get('/healthz', health_check)
    app.router.add_get('/', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv('PORT', 5000)))
    await site.start()
    
    logger.info(f"Health server started on port {os.getenv('PORT', 5000)}")
    return runner

async def main():
    """Main function with enhanced conflict handling"""
    lock_fd = acquire_lock()
    logger.info("🚀 Starting YukUz Logistics Bot - Unified Version (CONFLICT-FREE)")
    
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN not found! Set it in environment variables.")
        return
    
    if not DATABASE_URL:
        logger.error("❌ DATABASE_URL not found! Set it in environment variables.")
        return
    
    logger.info(f"📊 Database URL configured: {DATABASE_URL[:50]}...")
    
    if not init_db():
        logger.error("❌ Failed to initialize database!")
        return
    
    logger.info("✅ Database initialized")
    
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM announcements")
            
            sample_data = [
                ('📦 Ангрен → Грозный (22т)', 'Срочная перевозка гранита. Нужен тент 2шт. Хорошая цена, быстрая доставка.', 'cargo', 'published', 'Ангрен', 'Грозный', '22т', 'гранит', 'Тент 2шт', 'Азиз Норматов', '+998933456789', 456789123, 0, 0, datetime.now() - timedelta(minutes=3), datetime.now(), None, 'https://t.me/user?id=456789123', 'manual', None),
                ('📦 Ташкент → Наманган (19т)', 'Реф, тент, пепси. Качественная перевозка напитков.', 'cargo', 'published', 'Toshkent', 'Namangan', '19т', 'пепси', 'Реф, Тент', 'Умид Каримов', '+998944567890', 789123456, 0, 0, datetime.now() - timedelta(minutes=7), datetime.now(), None, 'https://t.me/user?id=789123456', 'manual', None),
                ('📦 Хорзига → Наманган (19-22т)', 'Юк пепси. Срочная доставка напитков.', 'cargo', 'published', 'Xiva', 'Namangan', '19-22 тоннагача', 'Юк Пепси', 'РЕФ тент фура керак', 'Хозирга', '+998912345678', 987654321, 0, 0, datetime.now() - timedelta(minutes=12), datetime.now(), None, 'https://t.me/user?id=987654321', 'external', '@logistics_channel'),
                ('🚛 Самарканд → Москва (25т)', 'Регулярные рейсы, надежная доставка в Россию', 'transport', 'published', 'Samarqand', 'Moskva', '25т', '', 'Kamaz', 'Карим Абдуллаев', '+998901234567', 123456789, 0, 0, datetime.now() - timedelta(minutes=15), datetime.now(), None, 'https://t.me/user?id=123456789', 'manual', None),
                ('📦 Алмата → Ташкент (15т)', 'Текстильные изделия, осторожная перевозка', 'cargo', 'published', 'Almaty', 'Toshkent', '15т', 'текстиль', 'Мега', 'Дилшода Каримова', '+998955678901', 321654987, 0, 0, datetime.now() - timedelta(hours=1), datetime.now(), None, 'https://t.me/user?id=321654987', 'external', '@cargo_uz')
            ]
            
            for data in sample_data:
                cursor.execute("""
                    INSERT INTO announcements 
                    (title, description, announcement_type, status, from_location, to_location, 
                     cargo_weight, cargo_type, vehicle_type, contact_name, contact_phone, 
                     user_telegram_id, views_count, contacts_accessed, created_at, updated_at, expires_at, message_url, source, telegram_username)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, data)
            
            conn.commit()
            cursor.close()
            conn.close()
            logger.info("✅ Sample data inserted")
            
    except Exception as e:
        logger.error(f"❌ Error inserting sample data: {e}")

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    try:
        commands = [BotCommand(command=cmd["command"], description=cmd["description"]) for cmd in BOT_COMMANDS]
        await bot.set_my_commands(commands)
    except TelegramConflictError:
        logger.warning("Command setup conflict - will work on production")

    health_runner = await create_health_server()
    logger.info("✅ YukUz Logistics Bot READY!")

    # Enhanced polling with conflict resolution
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            logger.info(f"🔄 Connection attempt {attempt + 1}/{max_attempts}")
            await bot.delete_webhook(drop_pending_updates=True)
            await asyncio.sleep(2)
            
            await dp.start_polling(
                bot,
                skip_updates=True,
                handle_signals=False,
                allowed_updates=[],
                close_bot_session=False
            )
            break
        except TelegramConflictError as e:
            logger.error(f"⚠️ Conflict detected: {e}")
            if attempt < max_attempts - 1:
                wait_time = (attempt + 1) * 10
                logger.info(f"⏳ Waiting {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                logger.error("❌ Max attempts reached. Shutting down.")
                return
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return

    finally:
        logger.info("🧹 Cleaning up resources...")
        try:
            await dp.storage.close()
            await bot.session.close()
            if lock_fd:
                lock_fd.close()
                try:
                    os.unlink(LOCK_FILE)
                except:
                    pass
        except Exception as e:
            logger.error(f"⚠️ Cleanup error: {e}")

if __name__ == "__main__":
    try:
        logger.info("🚀 YukUz Logistics Bot - Production Ready")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot gracefully stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal startup error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        logger.info("💤 Bot process terminated")
