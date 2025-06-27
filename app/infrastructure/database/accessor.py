from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.settings import Settings


engine = create_async_engine(url=Settings().db_url, future=True, pool_pre_ping=True)

AsyncSessionFactory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def get_db_session():
    async with AsyncSessionFactory() as session:
        yield session
