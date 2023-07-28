from sqlmodel import select
from strawberry.types import Info

from app.v1.models.models import Ingredient
from app.v1.graphql_api.presentation.inputs import IngredientInput, IngredientUpdateInput
from app.v1.graphql_api.controllers.exceptions import EXCEPTIONS, DBObjectNotFoundError, DBObjectALreadyExistsError


class CreateIngredientMutation:
    async def create_ingredient(self, info: Info, ingredient_data: IngredientInput):
        async with info.context.db() as session:
            db_ingredient = await session.exec(select(Ingredient).where(Ingredient.name==ingredient_data.name))
            ingredient = db_ingredient.first()
            if ingredient:
                raise DBObjectALreadyExistsError(
                    EXCEPTIONS["INGREDIENT"]["name_already_exists"]
                )
            ingredient = Ingredient(
                name=ingredient_data.name,
                measure_unit=ingredient_data.measure_unit
            )
            session.add(ingredient)
            await session.commit()
            await session.refresh(ingredient)
        return ingredient
    
    async def update_ingredient(self, info: Info, ingredient_data: IngredientUpdateInput):
        async with info.context.db() as session:
            db_ingredient = await session.exec(select(Ingredient).where(Ingredient.id==ingredient_data.id))
            ingredient = db_ingredient.first()
            if not ingredient:
                raise DBObjectNotFoundError(
                    EXCEPTIONS["INGREDIENT"]["id_does_not_exist"]
                )
            ingredient.name = ingredient_data.name
            ingredient.measure_unit = ingredient_data.measure_unit
            session.add(ingredient)
            await session.commit()
            await session.refresh(ingredient)
        return ingredient
