#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified run.py for Render deployment
- Telegram bot + health-check server
- Lock file protection
"""

import asyncio
import logging
import sys
import os
import atexit
from aiohttp import web
from aiohttp.web import Application, Request, Response

# ======== LOCK FILE ========
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
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ======== HEALTH CHECK ========
async def health_check(_: Request) -> Response:
    return web.Response(text="Bot is running", status=200)

async def start_health_server():
    app = Application()
    app.router.add_get("/healthz", health_check)
    app.router.add_get("/", health_check)
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"✅ Health-check server running on port {port}")

# ======== TELEGRAM BOT MAIN ========
# Вставляем сюда содержимое бывшего app/main.py:
import sys
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

# ... остальной код из main.py (создание бота, диспетчера, команд, middlewares, on_startup, on_shutdown)

async def bot_main():
    from app.config import get_config
    from app.db import init_db
    from app.middlewares import DatabaseMiddleware, LoggingMiddleware
    from app.routers import admin, cargo, search, start, transport, language

    config = get_config()
    if not config.BOT_TOKEN:
        raise ValueError("BOT_TOKEN is required")

    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
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

    dp.startup.register(lambda _: init_db())
    dp.startup.register(lambda _: logger.info("Bot startup done"))
    dp.shutdown.register(lambda _: bot.session.close())

    logger.info("🚛 Starting Telegram bot...")
    await dp.start_polling(bot)

# ======== MAIN ========
async def main():
    await start_health_server()
    await bot_main()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stopped by user")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        sys.exit(1)
