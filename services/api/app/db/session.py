from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
AsyncSessionLocal = async_session  # alias for explicit imports


async def get_db():
    async with async_session() as session:
        yield session
