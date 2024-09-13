from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import Config
from contextlib import asynccontextmanager

# Use `create_async_engine` for async operations
async_engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)

# Define session factory outside the function
AsyncSessionFactory = sessionmaker(
    bind=async_engine.sync_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Initialize the database
async def init_db():
    async with async_engine.begin() as conn:
        from src.books.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)

# Context manager to provide the session

@asynccontextmanager
async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=engine,  # change async_engine to engine
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session
