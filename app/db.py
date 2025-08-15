from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
from .config import get_config

class Base(DeclarativeBase):
    pass

_engine = None
_Session: async_sessionmaker[AsyncSession] | None = None

async def init_db():
    global _engine, _Session
    config = get_config()
    _engine = create_async_engine(config.DATABASE_URL, echo=False, future=True)
    _Session = async_sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    assert _Session is not None, "DB not initialized"
    return _Session()

async def ping() -> bool:
    session = await get_session()
    try:
        r = await session.execute(text("SELECT 1"))
        return r.scalar() == 1
    finally:
        await session.close()
