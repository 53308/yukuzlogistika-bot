"""
Main entry point for the Yukuz Logistics Telegram Bot
"""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from app.config import get_config
from app.db import init_db
from app.middlewares import DatabaseMiddleware, LoggingMiddleware
from app.routers import admin, cargo, search, start, transport, language

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

async def create_bot() -> Bot:
    """Create and configure bot instance"""
    config = get_config()

    if not config.BOT_TOKEN:
        raise ValueError("BOT_TOKEN is required. Please set it in .env file")

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    return bot

async def create_dispatcher() -> Dispatcher:
    """Create and configure dispatcher with routers and middlewares"""
    dp = Dispatcher(storage=MemoryStorage())

    # Add middlewares
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())

    # Include routers
    dp.include_router(start.router)
    dp.include_router(language.router)
    dp.include_router(cargo.router)
    dp.include_router(transport.router)
    dp.include_router(search.router)
    dp.include_router(admin.router)

    return dp

async def on_startup(bot: Bot) -> None:
    """Bot startup handler"""
    config = get_config()

    # Initialize database
    await init_db()
    logger.info("Database initialized")

    # Set bot commands
    from aiogram.types import BotCommand
    commands = [
        BotCommand(command="start", description="🏠 Бошлаш / Начать"),
        BotCommand(command="cargo", description="📦 Юк эълон қилиш / Объявить груз"),
        BotCommand(command="transport", description="🚛 Транспорт эълон қилиш / Объявить транспорт"),
        BotCommand(command="search", description="🔍 Қидириш / Поиск"),
        BotCommand(command="help", description="❓ Ёрдам / Помощь"),
    ]

    await bot.set_my_commands(commands)
    logger.info("Bot commands set")

    # Notify admins about bot startup
    if config.ADMINS:
        for admin_id in config.ADMINS:
            try:
                await bot.send_message(
                    admin_id,
                    "🤖 <b>Yukuz Logistics Bot запущен!</b>\n\n"
                    "✅ База данных инициализирована\n"
                    "✅ Команды установлены\n"
                    "✅ Бот готов к работе"
                )
            except Exception as e:
                logger.warning(f"Failed to notify admin {admin_id}: {e}")

    logger.info("Bot started successfully")

async def on_shutdown(bot: Bot) -> None:
    """Bot shutdown handler"""
    logger.info("Bot shutting down...")
    await bot.session.close()

async def main() -> None:
    """Main function"""
    logger.info("🚛 Starting Yukuz Logistics Bot...")

    try:
        # Create bot and dispatcher
        bot = await create_bot()
        dp = await create_dispatcher()

        # Register startup and shutdown handlers
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

        # Start polling
        logger.info("Starting Telegram bot...")
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise
