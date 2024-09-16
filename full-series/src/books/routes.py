from fastapi import APIRouter, Header, status, Depends
from fastapi.exceptions import HTTPException
from .schemas import *
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.books.service import BookService
from typing import List
from src.auth.dependencies import AccessTokenBearer, RoleChecker

book_service = BookService()
book_router = APIRouter()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(['admin', 'users']))

@book_router.get('/', response_model=List[Book], dependencies=[role_checker])
async def get_all_books(session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    
    return await book_service.get_all_books(session) # type: ignore

@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[role_checker])
async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session), token_detail:dict =Depends(access_token_bearer)):
    user_id = token_detail.get['user']['user_uid'] # type: ignore
    return await book_service.create_book(book_data, user_id, session) # type: ignore

@book_router.get('/{book_id}', response_model=Book, dependencies=[role_checker])
async def get_book(book_id: int, session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)) -> Book:
    book = await book_service.get_book(book_id, session) # type: ignore
    if book:
        return book # type: ignore
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

@book_router.patch("/{book_id}", response_model=Book, dependencies=[role_checker])
async def update_book(book_id: int, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)) -> Book:
    updated_book = await book_service.update_book(book_id, book_update_data, session) # type: ignore
    if updated_book:
        return updated_book # type: ignore
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(book_id: int, session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    deleted_book = await book_service.delete_book(book_id, session) # type: ignore
    if not deleted_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
