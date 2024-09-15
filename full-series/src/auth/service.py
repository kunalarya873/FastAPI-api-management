from .models import User
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import generate_passwd_hash
from .schemas import UserCreateModel
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        return user is not None

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.dict()  # Changed to `dict()` for compatibility
        user_data_dict['password_hash'] = generate_passwd_hash(user_data_dict['password'])  # Hash the password
        del user_data_dict['password']  # Remove plain password from dict

        new_user = User(**user_data_dict)

        try:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
        except SQLAlchemyError as e:
            await session.rollback()
            raise e  # Optionally, log the error here

        return new_user
