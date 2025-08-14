import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .config import Settings
from .db import init_db
from .middlewares import ThrottleMiddleware
from .routers import common, post_load, post_truck, search, admin

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")

async def main():
    settings = Settings.load()
    if not settings.bot_token:
        raise RuntimeError("BOT_TOKEN is empty")

    from aiogram.client.bot import DefaultBotProperties

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    dp = Dispatcher(storage=MemoryStorage())

    # middlewares
    dp.message.middleware(ThrottleMiddleware(rate_seconds=2))

    # routers
    dp.include_router(common.router)
    dp.include_router(post_load.router)
    dp.include_router(post_truck.router)
    dp.include_router(search.router)
    dp.include_router(admin.router)

    await init_db(settings)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
