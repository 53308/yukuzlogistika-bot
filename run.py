#!/usr/bin/env python3
"""
Production run.py for Render deployment with HTTP health check
"""

import asyncio
import logging
import sys
import os
from aiohttp import web
from aiohttp.web import Application, Request, Response
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import get_config
from app.db import init_db
from app.middlewares import DatabaseMiddleware, LoggingMiddleware
from app.routers import start

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Health check endpoint
async def health_check(_: Request) -> Response:
    return web.Response(text="Bot is running", status=200)

async def create_bot() -> Bot:
    """Create bot instance"""
    config = get_config()
    if not config.BOT_TOKEN:
        raise ValueError("BOT_TOKEN is required")
    
    return Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

async def create_dispatcher() -> Dispatcher:
    """Create dispatcher with middlewares and routers"""
    dp = Dispatcher(storage=MemoryStorage())
    
    # Add middlewares
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
    
    # Include routers
    dp.include_router(start.router)
    
    return dp

async def setup_bot(bot: Bot) -> None:
    """Initialize database and set commands"""
    await init_db()
    logger.info("Database initialized")
    
    # Set bot commands
    from aiogram.types import BotCommand
    commands = [
        BotCommand(command="start", description="🏠 Начать / Boshlaш"),
        BotCommand(command="help", description="❓ Помощь / Yordam"),
    ]
    await bot.set_my_commands(commands)
    logger.info("Bot commands set")

async def main():
    """Main function"""
    load_dotenv()
    logger.info("🚛 Starting Yukuz Logistics Bot...")
    
    try:
        # Create bot and dispatcher
        bot = await create_bot()
        dp = await create_dispatcher()
        
        # Setup bot
        await setup_bot(bot)
        
        # Create HTTP server for health checks
        app = Application()
        app.router.add_get('/', health_check)
        app.router.add_get('/healthz', health_check)
        
        # Get port from environment
        port = int(os.environ.get('PORT', 8080))
        
        # Start HTTP server
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', port)
        await site.start()
        logger.info(f"✅ HTTP server started on port {port}")
        
        # Start bot polling (this will run indefinitely)
        logger.info("🤖 Starting bot polling...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        sys.exit(1)
