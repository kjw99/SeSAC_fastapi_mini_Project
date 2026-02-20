from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from studyroom.models.user import User


class UserRepository:
    def save(self, db: Session, user: User):
        db.add(user)
        return user

    async def find_by_hakbun(self, db: AsyncSession, hakbun: str):
        stmt = select(User).where(User.hakbun == hakbun)
        result = await db.scalars(stmt)
        return result.first()

    def find_by_id(self, db: Session, user_id: int):
        return db.get(User, user_id)


user_repository = UserRepository()
