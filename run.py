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
from aiohttp.web import Application, Request, Response

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
    handlers=[logging.StreamHandler(sys.stdout)]
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
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"✅ Health-check server running on port {port}")
    return runner

# ======== BOT MAIN ========
async def bot_main():
    try:
        from app.main import main  # твой полный bot main
        await main()
    except Exception as e:
        logger.error(f"Bot error: {e}")
        raise

# ======== MAIN ========
async def main():
    logger.info("🚛 Starting Yukuz Logistics Bot on Render...")

    # Запускаем health-check сервер
    await create_health_server()

    # Запускаем бот параллельно
    await bot_main()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stopped by user")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        sys.exit(1)
