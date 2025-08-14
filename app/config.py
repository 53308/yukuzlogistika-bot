from pydantic import BaseModel, Field
import os

class Settings(BaseModel):
    bot_token: str = Field(validation_alias="BOT_TOKEN")
    admins: list[int] = Field(default_factory=list, validation_alias="ADMINS")
    channel_id: int | None = Field(default=None, validation_alias="CHANNEL_ID")
    database_url: str = Field(default="sqlite+aiosqlite:///./app/data.db", validation_alias="DATABASE_URL")

    @classmethod
    def load(cls) -> "Settings":
        admins_env = os.getenv("ADMINS", "")
        admins = [int(x) for x in admins_env.split(",") if x.strip().isdigit()]
        return cls(
            bot_token=os.getenv("BOT_TOKEN", ""),
            admins=admins,
            channel_id=int(os.getenv("CHANNEL_ID")) if os.getenv("CHANNEL_ID") else None,
            database_url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app/data.db"),
        )
