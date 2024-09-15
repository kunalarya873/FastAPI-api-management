from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class Book(BaseModel):
    uid: UUID
    title: str
    author: str
    publisher: str
    published_date: str  # Define this as a string
    page_count: int
    language: str
    created_at: str  # Also make this a string
    updated_at: str  # And this one too

    @classmethod
    def from_orm(cls, book):
        return cls(
            uid=book.uid,
            title=book.title,
            author=book.author,
            publisher=book.publisher,
            published_date=book.published_date.strftime('%Y-%m-%d'),  # Convert to string
            page_count=book.page_count,
            language=book.language,
            created_at=book.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Convert to string
            updated_at=book.updated_at.strftime('%Y-%m-%d %H:%M:%S')   # Convert to string
        )

    class Config:
        orm_mode = True