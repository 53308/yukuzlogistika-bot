from pydantic import BaseModel, Field
import os

class Settings(BaseModel):
    bot_token: str
    admins: list[int] = []
    channel_id: int | None = None
    database_url: str = "sqlite+aiosqlite:///./app/data.db"

    @classmethod
    def load(cls) -> "Settings":
        bot_token = os.getenv("BOT_TOKEN")
        if not bot_token:
            raise RuntimeError("BOT_TOKEN не задан в переменных окружения!")
        admins = [int(x) for x in os.getenv("ADMINS", "").split(",") if x.strip().isdigit()]
        channel_id = int(os.getenv("CHANNEL_ID")) if os.getenv("CHANNEL_ID") else None
        database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app/data.db")
        return cls(
            bot_token=bot_token,
            admins=admins,
            channel_id=channel_id,
            database_url=database_url
        )
