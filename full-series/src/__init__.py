#uvicorn src:app
from src.books.routes import book_router
from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import AsyncIterator
from src.db.main import init_db
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("Server is starting...")
    await init_db()
    yield
    print("Server has been stopped...")


version = "v1"
app = FastAPI(
    title="Books API",
    description="API for books management",
    version=version,
    lifespan=lifespan
)

app.include_router(book_router, prefix="/api/{version}/books", tags=['books'])