"""
Clean version of main.py without conflicts
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
from app.routers import start

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

    # Include only start router to avoid conflicts
    dp.include_router(start.router)

    return dp

async def main() -> None:
    """Main function"""
    logger.info("🚛 Starting Clean Yukuz Logistics Bot...")

    try:
        # Initialize database
        await init_db()
        logger.info("Database initialized")

        # Create bot and dispatcher
        bot = await create_bot()
        dp = await create_dispatcher()

        # Set bot commands
        from aiogram.types import BotCommand
        commands = [
            BotCommand(command="start", description="🏠 Boshlaш / Начать"),
            BotCommand(command="help", description="❓ Yordam / Помощь"),
        ]

        await bot.set_my_commands(commands)
        logger.info("Bot commands set")

        logger.info("Bot started successfully")

        # Start polling
        logger.info("Starting Telegram bot...")
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
