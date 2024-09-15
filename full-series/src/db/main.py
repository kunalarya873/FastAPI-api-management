from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config import Config
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

# Create async engine
async_engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)

# Session factory for async session
from sqlalchemy import create_engine

engine = create_engine(Config.DATABASE_URL, echo=True)

AsyncSessionFactory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Initialize the database
async def init_db():
    async with async_engine.begin() as conn:
        from src.books.models import Book
        from src.auth.models import User 
        await conn.run_sync(SQLModel.metadata.create_all)

@asynccontextmanager
async def get_session():
    session = AsyncSessionFactory()
    try:
        yield session  # Yield the session to be used in the context
        await session.commit()  # Commit after the context is exited
    except Exception as e:
        await session.rollback()  # Rollback if there is an exception
        raise e  # Optionally, log or handle the error here
    finally:
        await session.close()  # Always close the session

