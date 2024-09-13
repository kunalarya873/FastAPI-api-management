from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import  datetime
import uuid
class Book(SQLModel, table=True):
    uid: uuid.UUID = Field(
        sa_column= Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4
        )
    )
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime = Field(Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime= Field(Column(pg.TIMESTAMP, default=datetime.now()))

    def __repr__(self):
        return f"<Book {self.title}>"