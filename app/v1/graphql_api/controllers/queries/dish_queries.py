from strawberry.types import Info

from app.v1.graphql_api.presentation.inputs import IngredientsInput
from app.v1.graphql_api.presentation.schemas import DishType


class DishQueries:
    async def get_all_dishes(self, info: Info) -> list[DishType]:
        return await info.context.dish_dao.get_list()

    async def get_dish(self, info: Info, dish_id: int) -> DishType:
        return await info.context.dish_dao.get(dish_id)

    async def get_dishes_by_ingredients(
        self,
        info: Info,
        ingredients: IngredientsInput,
    ):
        return await info.context.dish_dao.get_dishes_by_ingredients(ingredients)
