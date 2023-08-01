from strawberry.types import Info

from app.v1.graphql_api.presentation.inputs import DishInput, DishUpdateInput
from app.v1.models.models import Dish


class DishMutation:
    async def create_dish(self, info: Info, dish_data: DishInput) -> list[Dish]:
        return await info.context.dish_dao.create(dish_data)

    async def update_dish(self, info: Info, dish_data: DishUpdateInput) -> Dish:
        return await info.context.dish_dao.update(dish_data)

    async def delete_dish(self, info: Info, dish_id: int) -> list[Dish]:
        return await info.context.dish_dao.delete(dish_id)
