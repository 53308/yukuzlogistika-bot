#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified run.py for Render deployment
- Runs Telegram bot  
- Runs health-check server for Render
- Prevents multiple instances via lock file
"""

import asyncio
import logging
import sys
import os
import atexit
import threading
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

# ======== LOCK FILE PROTECTION ========
LOCK_FILE = "/tmp/yukuz_bot.lock"
if os.path.exists(LOCK_FILE):
    print("⚠️ Bot is already running. Exiting...")
    sys.exit(0)

with open(LOCK_FILE, "w") as f:
    f.write(str(os.getpid()))

@atexit.register
def cleanup():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

# ======== LOGGING ========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

# ======== HEALTH CHECK ========
async def health_check(_: Request) -> Response:
    return web.Response(text="Bot is running", status=200)

async def create_health_server():
    app = Application()
    app.router.add_get("/healthz", health_check)
    app.router.add_get("/", health_check)
    port = int(os.environ.get("PORT", 8080))
    return web.AppRunner(app), port

# ======== BOT LOGIC ========
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
        BotCommand(command="help", description="❓ Ёрдам / Помощь"),
    ]
    await bot.set_my_commands(commands)

    logger.info("Bot commands set")
    logger.info("Bot started successfully")

async def on_shutdown(bot: Bot) -> None:
    """Bot shutdown handler"""
    logger.info("Bot shutting down...")
    await bot.session.close()

async def bot_main():
    """Start the bot polling"""
    load_dotenv()
    bot = await create_bot()
    dp = await create_dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)

# ======== BOT RUNNER ========
def run_bot_in_thread():
    def run_bot():
        try:
            asyncio.run(bot_main())
        except Exception as e:
            logger.error(f"Bot thread error: {e}")

    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("Bot started in background thread")

# ======== MAIN ========
async def main():
    logger.info("🚛 Starting Yukuz Logistics Bot on Render...")

    try:
        run_bot_in_thread()
        await asyncio.sleep(2)  # Give bot time to start

        runner, port = await create_health_server()
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        logger.info(f"✅ Health-check server running on port {port}")

        while True:
            await asyncio.sleep(1)

    except Exception as e:
        logger.error(f"Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stopped by user")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        sys.exit(1)
