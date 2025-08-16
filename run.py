#!/usr/bin/env python3
"""
Main bot runner with proper architecture
Exact copy of @yuk_uz_logistika_bot
"""

import asyncio
import logging
import os
import threading
import time
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

# Import configuration and models
import os

# Get BOT_TOKEN directly from environment
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Bot commands
BOT_COMMANDS = [
    {"command": "start", "description": "🏠 Главное меню"},
    {"command": "cargo", "description": "📦 Найти груз"},
    {"command": "transport", "description": "🚛 Найти транспорт"},
    {"command": "search", "description": "🔍 Поиск"},
    {"command": "help", "description": "ℹ️ Помощь"}
]
from app.models import init_db

# Import routers
from app.routers import start, search, help

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

# Health check server for Render
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
    """Main function"""
    logger.info("🚀 Starting YukUz Logistics Bot - EXACT COPY")
    
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN not found!")
        logger.error(f"Current BOT_TOKEN value: {BOT_TOKEN}")
        return
    
    # Initialize database
    if not init_db():
        logger.error("❌ Failed to initialize database!")
        return
    
    logger.info("✅ Database initialized")
    
    # Insert sample data
    try:
        from app.models import get_db_connection
        from datetime import datetime, timedelta
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Clear existing data and insert samples
        cursor.execute("DELETE FROM announcements")
        
        sample_data = [
            ('📦 Ангрен → Грозный (22т)', 'Срочная перевозка гранита. Нужен тент 2шт. Хорошая цена, быстрая доставка.', 'cargo', 'published', 'Ангрен', 'Грозный', '22т', 'гранит', 'Тент 2шт', 'Азиз Норматов', '+998933456789', 456789123, 0, 0, datetime.now() - timedelta(minutes=3), datetime.now(), None, 'https://t.me/user?id=456789123'),
            
            ('📦 Ташкент → Наманган (19т)', 'Реф, тент, пепси. Качественная перевозка напитков.', 'cargo', 'published', 'Ташкент', 'Наманган', '19т', 'пепси', 'Реф, Тент', 'Умид Каримов', '+998944567890', 789123456, 0, 0, datetime.now() - timedelta(minutes=7), datetime.now(), None, 'https://t.me/user?id=789123456'),
            
            ('📦 Хорзига → Наманган (19-22т)', 'Юк пепси. Срочная доставка напитков.', 'cargo', 'published', 'Хорзига', 'Наманган', '19-22 тоннагача', 'Юк Пепси', 'РЕФ тент фура керак', 'Хозирга', '+998912345678', 987654321, 0, 0, datetime.now() - timedelta(minutes=12), datetime.now(), None, 'https://t.me/user?id=987654321'),
            
            ('🚛 Самарканд → Москва (25т)', 'Регулярные рейсы, надежная доставка в Россию', 'transport', 'published', 'Самарканд', 'Москва', '25т', '', 'Kamaz', 'Карим Абдуллаев', '+998901234567', 123456789, 0, 0, datetime.now() - timedelta(minutes=15), datetime.now(), None, 'https://t.me/user?id=123456789'),
            
            ('📦 Алмата → Ташкент (15т)', 'Текстильные изделия, осторожная перевозка', 'cargo', 'published', 'Алмата', 'Ташкент', '15т', 'текстиль', 'Мега', 'Дилшода Каримова', '+998955678901', 321654987, 0, 0, datetime.now() - timedelta(hours=1), datetime.now(), None, 'https://t.me/user?id=321654987')
        ]
        
        for data in sample_data:
            cursor.execute("""
                INSERT INTO announcements 
                (title, description, announcement_type, status, from_location, to_location, 
                 cargo_weight, cargo_type, vehicle_type, contact_name, contact_phone, 
                 user_telegram_id, views_count, contacts_accessed, created_at, updated_at, expires_at, message_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, data)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("✅ Sample data inserted")
        
    except Exception as e:
        logger.error(f"❌ Error inserting sample data: {e}")
    
    # Create bot
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    
    # Include routers
    dp.include_router(start.router)
    dp.include_router(search.router)
    dp.include_router(help.router)
    
    # Set commands
    commands = [BotCommand(command=cmd["command"], description=cmd["description"]) for cmd in BOT_COMMANDS]
    await bot.set_my_commands(commands)
    
    # Start health server
    health_runner = await create_health_server()
    
    # Start external group integration in background
    try:
        from app.group_integration import start_external_integration
        integration_task = asyncio.create_task(start_external_integration())
        logger.info("🔄 External group integration started")
    except Exception as e:
        logger.warning(f"⚠️ Could not start external integration: {e}")
    
    logger.info("✅ YukUz Logistics Bot READY!")
    logger.info("📱 Features: Exact copy with proper architecture, menu, search, details + external group integration")
    
    try:
        # Start polling
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Error: {e}")
    finally:
        # Cleanup
        await health_runner.cleanup()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
