from typing import List

from sqlmodel import select
from strawberry.types import Info

from app.v1.models.models import Dish
from app.v1.graphql_api.presentation.schemas import DishType
from app.v1.graphql_api.controllers.exceptions import EXCEPTIONS, DBObjectNotFoundError


class DishQueries:
    async def get_all_dishes(self, info: Info) -> List[DishType]:
        async with info.context.db() as session:
            db_dishes = await session.exec(select(Dish))
        return db_dishes.all()
    
    async def get_dish(self, info: Info, dish_id: int) -> DishType:
        async with info.context.db() as session:
            db_dishes = await session.exec(select(Dish).where(Dish.id==dish_id))
            dish = db_dishes.first()
            if not dish:
                raise DBObjectNotFoundError(
                    EXCEPTIONS["DISH"]["id_does_not_exist"]
                )
        return dish
