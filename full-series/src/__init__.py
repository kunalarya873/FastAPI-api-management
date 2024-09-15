from fastapi import FastAPI
from typing import AsyncIterator
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routers import auth_router
from src.books.routes import book_router

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

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
