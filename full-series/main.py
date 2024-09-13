#fastapi dev main.py
from fastapi import FastAPI
from src.books.routes import book_router

version = "v1"
app = FastAPI(
    title="Books API",
    description="API for books management",
    version=version
)

app.include_router(book_router, prefix="/api/{version}/books", tags=['books'])