from typing import List

from sqlmodel import select
from strawberry.types import Info

from app.v1.models.models import Ingredient
from app.v1.graphql_api.presentation.schemas import IngredientType
from app.v1.graphql_api.controllers.exceptions import EXCEPTIONS, DBObjectNotFoundError


class IngredientQueries:    
    async def get_all_ingredients(self, info: Info) -> List[IngredientType]:
        async with info.context.db() as session:
            db_ingredients = await session.exec(select(Ingredient))
        return db_ingredients.all()
    
    async def get_ingredient(self, info: Info, ingredient_id: int) -> IngredientType:
        async with info.context.db() as session:
            db_ingredients = await session.exec(select(Ingredient).where(Ingredient.id==ingredient_id))
            ingredient = db_ingredients.first()
            if not ingredient:
                raise DBObjectNotFoundError(
                    EXCEPTIONS["INGREDIENT"]["id_does_not_exist"]
                )
        return ingredient
