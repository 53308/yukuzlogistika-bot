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
from aiohttp import web
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import get_config
from app.db import init_db
from app.middlewares import DatabaseMiddleware, LoggingMiddleware
from app.routers import admin, cargo, search, start, transport, language

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
async def health_check(_: web.Request) -> web.Response:
    return web.Response(text="Bot is running", status=200)

async def create_health_server():
    app = web.Application()
    app.router.add_get("/healthz", health_check)
    app.router.add_get("/", health_check)
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"✅ Health-check server running on port {port}")

# ======== BOT LOGIC ========
async def create_bot() -> Bot:
    config = get_config()
    if not config.BOT_TOKEN:
        raise ValueError("BOT_TOKEN is required. Please set it in .env file")

    return Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

async def create_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())

    dp.include_router(start.router)
    dp.include_router(language.router)
    dp.include_router(cargo.router)
    dp.include_router(transport.router)
    dp.include_router(search.router)
    dp.include_router(admin.router)

    return dp

async def on_startup(bot: Bot):
    config = get_config()
    await init_db()
    logger.info("Database initialized")

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

async def on_shutdown(bot: Bot):
    logger.info("Bot shutting down...")
    await bot.session.close()

async def main():
    load_dotenv()
    bot = await create_bot()
    dp = await create_dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Запуск health-check сервера
    await create_health_server()

    # Запуск бота в том же asyncio loop
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stopped by user")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        sys.exit(1)
