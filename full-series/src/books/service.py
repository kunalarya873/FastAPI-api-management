from datetime import datetime
from uuid import UUID
from fastapi import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import Book
from .schemas import BookCreateModel, BookUpdateModel

def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_user_books(self, user_uid: UUID, session: AsyncSession):
        statement = (
            select(Book)
            .order_by(desc(Book.created_at))
        )
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()

        if book:
            # Convert datetime fields to string
            book.published_date = book.published_date.strftime("%Y-%m-%d") # type: ignore
            book.created_at = book.created_at.strftime("%Y-%m-%d %H:%M:%S") # type: ignore
            book.updated_at = book.updated_at.strftime("%Y-%m-%d %H:%M:%S") # type: ignore
        
        return book

    async def create_book(self, book_data: BookCreateModel, user_uid:str, session: AsyncSession):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)
        new_book.published_date = datetime.strptime(
            book_data_dict["published_date"], "%Y-%m-%d"
        )

        new_book.user_uid = user_uid # type: ignore

        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)

        # Convert datetime fields to strings
        new_book.published_date = format_datetime(new_book.published_date) # type: ignore
        new_book.created_at = format_datetime(new_book.created_at) # type: ignore
        new_book.updated_at = format_datetime(new_book.updated_at) # type: ignore

        return new_book
    
    async def update_book(
        self, book_uid: UUID, update_data: BookUpdateModel, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_uid, session) # type: ignore

        if book_to_update:
            update_data_dict = update_data.model_dump()

            for k, v in update_data_dict.items():
                setattr(book_to_update, k, v)

            await session.commit()
            await session.refresh(book_to_update)

            return book_to_update
        else:
            raise HTTPException(status_code=404, detail="Book not found")

    async def delete_book(self, book_uid: UUID, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session) # type: ignore

        if book_to_delete:
            await session.delete(book_to_delete)
            await session.commit()
            return {}
        else:
            return None
