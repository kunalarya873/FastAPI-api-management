from sqlmodel import SQLModel, Field, Column
import uuid
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users" # type: ignore
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True), 
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4
    )
)
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(Column(
        pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow))
    def __repr__(self) -> str:
        return f"<User {self.username}>"