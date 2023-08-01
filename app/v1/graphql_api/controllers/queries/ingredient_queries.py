from strawberry.types import Info

from app.v1.models.models import Ingredient


class IngredientQueries:
    async def get_all_ingredients(self, info: Info) -> list[Ingredient]:
        return await info.context.ingredient_dao.get_list()

    async def get_ingredient(self, info: Info, ingredient_id: int) -> Ingredient:
        return await info.context.ingredient_dao.get(ingredient_id)
