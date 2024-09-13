from fastapi import APIRouter, Header, status, Depends
from fastapi.exceptions import HTTPException
from .schemas import *
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.books.service import BookService
from typing import List

book_service = BookService()
book_router = APIRouter()

@book_router.get('/', response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    return await book_service.get_all_books(session)

@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)):
    return await book_service.create_book(book_data, session)

@book_router.get('/{book_id}', response_model=Book)
async def get_book(book_id: int, session: AsyncSession = Depends(get_session)) -> Book:
    book = await book_service.get_book(book_id, session)
    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

@book_router.patch("/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session)) -> Book:
    updated_book = await book_service.update_book(book_id, book_update_data, session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, session: AsyncSession = Depends(get_session)):
    deleted_book = await book_service.delete_book(book_id, session)
    if not deleted_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
