from fastapi import APIRouter, Header, status
from fastapi.exceptions import HTTPException
from .books_data import books
from .schemas import *
from typing import Optional, List
book_router = APIRouter()

@book_router.get("/hello_world")
async def read_root():
    return {"message": "Hello World"}

@book_router.get('/greet/{name}')
async def greet(name: Optional[str]="User") -> dict:
    return {"message": f"Hello {name}"}


@book_router.post("/create_book")
async def create_book(book_data: Book):
    return {
        "title": book_data.title,
        "author": book_data.author
    }

@book_router.get('/get_headers')
async def get_headers(
        accept:str = Header(None),
        content_type: str= Header(None),
        user_agent: str = Header(None),
        host:str = Header(None)
):
    return {
        "Accept": accept,
        "Content-Type": content_type,
        "user_agent": user_agent,
        "host": host,
    }


@book_router.get('/', response_model=List[Book])
async def get_all_books():
    return books

@book_router.post('/books', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data:Book)-> dict :
    #new_book = book_data.model_dump()
    new_book = book_data.dict()
    books.append(new_book)
    return new_book

@book_router.get('/books/{book_id}')
async def get_book(book_id: int)-> dict:
    for book in books:
        if book["id"] == book_id:
            return book
        
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="book not found"
    )


book_router.patch("/book/{book_id}")
async def update_book(book_id: int, book_update_data: BookUpdateModel)-> dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language

            return book
    raise HTTPException(status_code=404, detail="Book not found")
