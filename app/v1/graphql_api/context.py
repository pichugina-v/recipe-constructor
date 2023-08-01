from fastapi import Depends
from strawberry.fastapi import BaseContext

from app.db.database import async_session_maker
from app.v1.dao.dish_dao import DishDAO
from app.v1.dao.ingredient_dao import IngredientDAO


class CustomContext(BaseContext):

    """Расширенный базовый класс BaseContext"""

    def __init__(self, dish_dao: DishDAO, ingredient_dao: IngredientDAO):
        self.dish_dao = dish_dao
        self.ingredient_dao = ingredient_dao


def custom_context_dependency() -> CustomContext:
    """Метод для инициализации CustomContext и передачи необходимых зависимостей"""

    return CustomContext(
        dish_dao=DishDAO(db=async_session_maker),
        ingredient_dao=IngredientDAO(db=async_session_maker),
    )


async def get_context(
    custom_context=Depends(custom_context_dependency),
):
    return custom_context
