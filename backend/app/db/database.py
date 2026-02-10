# Connection main library
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import URL,create_engine,text

# Connection inside package
from app.core.config import settings

# Create async_engine
engine = create_async_engine(
    settings.database_url, # DSN 
    pool_size=5,           #always-open connection
    max_overflow=10,       #additional connection
    echo=True,             #debugging that allows view query in console
)

# This is fabric session
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    async with async_session_maker() as session:
        # 100% close session if will be errors
        try:
            yield session
        finally:
            await session.close()