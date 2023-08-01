from strawberry.types import Info

from app.v1.graphql_api.presentation.inputs import (
    IngredientInput,
    IngredientUpdateInput,
)


class IngredientMutation:
    async def create_ingredient(self, info: Info, ingredient_data: IngredientInput):
        return await info.context.ingredient_dao.create(ingredient_data)

    async def update_ingredient(
        self,
        info: Info,
        ingredient_data: IngredientUpdateInput,
    ):
        return await info.context.ingredient_dao.update(ingredient_data)
