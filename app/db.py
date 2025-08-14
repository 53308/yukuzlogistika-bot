from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import text
from .config import get_config

class Base(DeclarativeBase):
    pass

_engine = None
_Session: sessionmaker | None = None

async def init_db():
    global _engine, _Session
    config = get_config()
    _engine = create_async_engine(config.DATABASE_URL, echo=False, future=True)
    _Session = sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    assert _Session is not None, "DB not initialized"
    return _Session()

async def ping() -> bool:
    async with (await get_session()) as s:
        r = await s.execute(text("SELECT 1"))
        return r.scalar() == 1
