from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.v1.dao.exceptions import (
    EXCEPTIONS,
    DBObjectALreadyExistsError,
    DBObjectNotFoundError,
)
from app.v1.graphql_api.presentation.inputs import (
    IngredientInput,
    IngredientUpdateInput,
)
from app.v1.models.models import Ingredient


class IngredientDAO:

    """DAO для ингредиента"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self) -> list[Ingredient]:
        """Метод для получения списка всех игредиентов"""

        async with self.db() as session:
            db_ingredients = await session.exec(select(Ingredient))
        return db_ingredients.all()

    async def get(self, ingredient_id: int) -> Ingredient:
        """Метод для получения ингредиента по ID"""

        async with self.db() as session:
            db_ingredients = await session.exec(
                select(Ingredient).where(Ingredient.id == ingredient_id),
            )
            ingredient = db_ingredients.first()
            if not ingredient:
                raise DBObjectNotFoundError(
                    EXCEPTIONS['INGREDIENT']['id_does_not_exist'],
                )
        return ingredient

    async def create(self, ingredient_data: IngredientInput) -> Ingredient:
        """Метод для создания игредиента"""

        async with self.db() as session:
            db_ingredient = await session.exec(
                select(Ingredient).where(
                    Ingredient.name == ingredient_data.name,
                ),
            )
            ingredient = db_ingredient.first()
            if ingredient:
                raise DBObjectALreadyExistsError(
                    EXCEPTIONS['INGREDIENT']['name_already_exists'],
                )
            ingredient = Ingredient(
                name=ingredient_data.name,
                measure_unit=ingredient_data.measure_unit,
            )
            session.add(ingredient)
            await session.commit()
            await session.refresh(ingredient)
        return ingredient

    async def update(self, ingredient_data: IngredientUpdateInput) -> Ingredient:
        """Метод для обновления игредиента"""

        async with self.db() as session:
            db_ingredient = await session.exec(
                select(Ingredient).where(Ingredient.id == ingredient_data.id),
            )
            ingredient = db_ingredient.first()
            if not ingredient:
                raise DBObjectNotFoundError(
                    EXCEPTIONS['INGREDIENT']['id_does_not_exist'],
                )
            ingredient.name = ingredient_data.name
            ingredient.measure_unit = ingredient_data.measure_unit
            session.add(ingredient)
            await session.commit()
            await session.refresh(ingredient)
        return ingredient
