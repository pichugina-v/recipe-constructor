from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.v1.dao.exceptions import (
    EXCEPTIONS,
    DBObjectALreadyExistsError,
    DBObjectNotFoundError,
)
from app.v1.graphql_api.presentation.inputs import (
    DishInput,
    DishUpdateInput,
    IngredientInput,
    IngredientsInput,
)
from app.v1.models.models import Dish, DishIngredientAmount, Ingredient


class DishDAO:

    """DAO для блюда"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self) -> list[Dish]:
        """Метод для получения списка всех блюд"""

        async with self.db() as session:
            db_dishes = await session.exec(select(Dish))
        return db_dishes.all()

    async def get(self, dish_id: int) -> Dish:
        """Метод для получения блюда по ID"""

        async with self.db() as session:
            db_dishes = await session.exec(select(Dish).where(Dish.id == dish_id))
            dish = db_dishes.first()
            if not dish:
                raise DBObjectNotFoundError(
                    EXCEPTIONS['DISH']['id_does_not_exist'],
                )
        return dish

    async def get_dishes_by_ingredients(
        self,
        ingredients: IngredientsInput,
    ) -> list[Dish]:
        """
        Метод для получения блюд по указанным ингредиентам.
        Возвращает блюдо, если в списке указанных игредиентов
        содержатся все ингредиенты, необходимые для приготовления блюда
        """

        async with self.db() as session:
            ingredients_names = [
                ingredient.ingredient.name
                for ingredient in ingredients.ingredient_amount
            ]
            db_ingredients = await session.exec(
                select(Ingredient).where(
                    Ingredient.name.in_(ingredients_names),
                ),
            )
            db_ingredients = db_ingredients.all()

            db_ingredients_ids = [ingredient.id for ingredient in db_ingredients]
            db_dishes = await session.exec(
                select(Dish)
                .join(Dish.ingredients)
                .where(Ingredient.id.in_(db_ingredients_ids))
                .distinct(),
            )

            result = []
            for db_dish in db_dishes.all():
                dish_ingredients = [ingredient.id for ingredient in db_dish.ingredients]
                if set(dish_ingredients).issubset(db_ingredients_ids):
                    result.append(db_dish)

            return result

    async def create(self, dish_data: DishInput) -> Dish:
        """Метод для создания блюда"""

        async with self.db() as session:
            db_dish = await session.exec(
                select(Dish).where(Dish.name == dish_data.name),
            )
            dish = db_dish.first()
            if dish:
                raise DBObjectALreadyExistsError(
                    EXCEPTIONS['DISH']['name_already_exists'],
                )
            dish = Dish(
                name=dish_data.name,
                text=dish_data.text,
            )
            session.add(dish)
            await session.commit()
            await session.refresh(dish)
            for ingredient_data in dish_data.ingredients:
                new_ingredient = await self._create_dish_ingredient(
                    session,
                    ingredient_data.ingredient,
                )
                await self._create_ingredient_amount(
                    session,
                    dish.id,
                    new_ingredient.id,
                    ingredient_data.amount,
                )
        return dish

    async def update(self, dish_data: DishUpdateInput) -> Dish:
        """Метод для обновления блюда"""

        async with self.db() as session:
            db_dish_by_name = await session.exec(
                select(Dish).where(Dish.name == dish_data.name),
            )
            dish_by_name = db_dish_by_name.first()
            if dish_by_name and not dish_data.ingredients:
                raise DBObjectALreadyExistsError(
                    EXCEPTIONS['DISH']['name_already_exists'],
                )
            db_dish = await session.exec(select(Dish).where(Dish.id == dish_data.id))
            dish = db_dish.first()
            if not dish:
                raise DBObjectNotFoundError(
                    EXCEPTIONS['DISH']['id_does_not_exist'],
                )
            dish.name = dish_data.name
            dish.text = dish_data.text
            session.add(dish)
            await session.commit()
            await session.refresh(dish)
            if dish_data.ingredients:
                await self._delete_ingredient_amount(session, dish.id)
                for ingredient_data in dish_data.ingredients:
                    updated_ingredient = await self._update_dish_ingredient(
                        session,
                        ingredient_data.ingredient,
                    )
                    if ingredient_data.amount:
                        await self._update_ingredient_amount(
                            session,
                            dish.id,
                            updated_ingredient.id,
                            ingredient_data.amount,
                        )
        return dish

    async def delete(self, dish_id: int) -> Dish:
        """
        Метод для удаления блюда.
        При удалении блюда удаляются только связи между ингредиентом и блюдом.
        Ингредиенты не удаляются
        """

        async with self.db() as session:
            db_dish = await session.exec(select(Dish).where(Dish.id == dish_id))
            dish = db_dish.first()
            if not dish:
                raise DBObjectNotFoundError(
                    EXCEPTIONS['DISH']['id_does_not_exist'],
                )
            await self._delete_ingredient_amount(session, dish_id)
            await session.delete(dish)
            await session.commit()

        return dish

    async def _create_dish_ingredient(
        self,
        session: AsyncSession,
        ingredient_data: IngredientInput,
    ) -> Ingredient:
        """Вспомогательный метод для создания ингредиентов при создании блюда"""

        db_ingredient = await session.exec(
            select(Ingredient).where(Ingredient.name == ingredient_data.name),
        )
        ingredient = db_ingredient.first()
        if ingredient:
            return ingredient
        ingredient = Ingredient(
            name=ingredient_data.name,
            measure_unit=ingredient_data.measure_unit,
        )
        session.add(ingredient)
        await session.commit()
        await session.refresh(ingredient)
        return ingredient

    async def _update_dish_ingredient(
        self,
        session: AsyncSession,
        ingredient_data: IngredientInput,
    ) -> Ingredient:
        """Вспомогательный метод для обновления ингредиентов при обновлении блюда"""

        db_ingredient = await session.exec(
            select(Ingredient).where(Ingredient.name == ingredient_data.name),
        )
        ingredient = db_ingredient.first()
        if ingredient:
            ingredient.measure_unit = ingredient_data.measure_unit
            session.add(ingredient)
            await session.commit()
            await session.refresh(ingredient)
            return ingredient
        return await self._create_dish_ingredient(session, ingredient_data)

    async def _create_ingredient_amount(
        self,
        session: AsyncSession,
        dish_id: int,
        ingredient_id: int,
        amount: int,
    ) -> None:
        """
        Вспомогательный метод для проставления связи M-T-M между ингредиентом и блюдом
        и сохранении данных о количестве ингредиента в блюде
        """

        ingredient_to_dish = DishIngredientAmount(
            dish_id=dish_id,
            ingredient_id=ingredient_id,
            amount=amount,
        )
        session.add(ingredient_to_dish)
        await session.commit()
        await session.refresh(ingredient_to_dish)

    async def _update_ingredient_amount(
        self,
        session: AsyncSession,
        dish_id: int,
        ingredient_id: int,
        amount: int,
    ) -> None:
        """
        Вспомогательный метод для обноления связи M-T-M между ингредиентом и блюдом
        и обновлении данных о количестве ингредиента в блюде
        """

        db_ingredient_amount = await session.exec(
            select(DishIngredientAmount).where(
                DishIngredientAmount.dish_id == dish_id,
                DishIngredientAmount.ingredient_id == ingredient_id,
            ),
        )
        ingredient_amount = db_ingredient_amount.first()
        if not ingredient_amount:
            await self._create_ingredient_amount(
                session,
                dish_id,
                ingredient_id,
                amount,
            )
        else:
            ingredient_amount.amount = amount
            session.add(ingredient_amount)
            await session.commit()
            await session.refresh(ingredient_amount)

    async def _delete_ingredient_amount(
        self,
        session: AsyncSession,
        dish_id: int,
    ) -> None:
        """
        Вспомогательный метод для удаления связи M-T-M между ингредиентом и блюдом
        и удаления информации о количестве игредиента в блюде
        """
        db_ingredients_amount = await session.exec(
            select(DishIngredientAmount).where(
                DishIngredientAmount.dish_id == dish_id,
            ),
        )
        ingredients_amount = db_ingredients_amount.all()
        for amount in ingredients_amount:
            await session.delete(amount)
            await session.commit()
