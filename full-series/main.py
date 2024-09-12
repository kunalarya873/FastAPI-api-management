#fastapi dev main.py
from fastapi import FastAPI, HTTPException, Header, status
from typing import Optional, List
from pydantic import BaseModel
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get('/greet/{name}')
async def greet(name: Optional[str]="User") -> dict:
    return {"message": f"Hello {name}"}

class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

@app.post("/create_book")
async def create_book(book_data: Book):
    return {
        "title": book_data.title,
        "author": book_data.author
    }

@app.get('/get_headers')
async def get_headers(
        accept:str = Header(None),
        content_type: str= Header(None),
        user_agent: str = Header(None),
        host:str = Header(None)
):
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["user_agent"] = user_agent
    request_headers["host"]= host
    return request_headers

books = [
    {
        "id": 1,
        "title": "HP",
        "author": "JK",
        "publisher": "penguin",
        "published_date": "1994",
        "page_count": 1222,
        "language": "english"
    },
    {
        "id": 2,
        "title": "JJ",
        "author": "ALK",
        "publisher": "oxford",
        "published_date": "2000",
        "page_count": 102,
        "language": "spanish"
    }
]


@app.get('/books', response_model=List[Book])
async def get_all_books():
    return books

@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data:Book)-> dict :
    #new_book = book_data.model_dump()
    new_book = book_data.dict()
    books.append(new_book)
    return new_book

@app.get('/books/{book_id}')
async def get_book(book_id: int)-> dict:
    for book in books:
        if book["id"] == book_id:
            return book
        
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="book not found"
    )

