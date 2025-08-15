#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified run.py for Render deployment
- Runs Telegram bot (from app/main.py)
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
    return web.AppRunner(app), port

# ======== BOT RUNNER ========
def run_bot_in_thread():
    async def bot_main():
        try:
            from app.main import main  # FULL bot version
            await main()
        except Exception as e:
            logger.error(f"Bot error: {e}")

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
        # Start bot in background thread
        run_bot_in_thread()

        # Give bot time to start
        await asyncio.sleep(2)

        # Start health-check server
        runner, port = await create_health_server()
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        logger.info(f"✅ Health-check server running on port {port}")

        # Keep running
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
