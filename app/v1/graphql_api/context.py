from fastapi import Depends
from strawberry.fastapi import BaseContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.database import async_session_maker


class CustomContext(BaseContext):
    def __init__(self, db: AsyncSession):
        self.db = db


def custom_context_dependency() -> CustomContext:
    return CustomContext(db=async_session_maker)


async def get_context(
    custom_context=Depends(custom_context_dependency),
):
    return custom_context
