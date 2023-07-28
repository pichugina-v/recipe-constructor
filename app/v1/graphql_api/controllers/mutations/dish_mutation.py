from strawberry.types import Info
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.v1.models.models import Dish, Ingredient, DishIngredientAmount
from app.v1.graphql_api.presentation.inputs import DishInput, DishUpdateInput, IngredientInput
from app.v1.graphql_api.controllers.exceptions import EXCEPTIONS, DBObjectNotFoundError, DBObjectALreadyExistsError


class CreateDishMutation:
    async def create_dish(self, info: Info, dish_data: DishInput):
        async with info.context.db() as session:
            db_dish = await session.exec(select(Dish).where(Dish.name==dish_data.name))
            dish = db_dish.first()
            if dish:
                raise DBObjectALreadyExistsError(
                    EXCEPTIONS["DISH"]["name_already_exists"]
                )
            dish = Dish(
                name=dish_data.name,
                text=dish_data.text
            )
            session.add(dish)
            await session.commit()
            await session.refresh(dish)
            for ingredient_data in dish_data.ingredients:
                new_ingredient = await self._create_dish_ingredient(session, ingredient_data.ingredient)
                await self._create_ingredient_amount(session, dish.id, new_ingredient.id, ingredient_data.amount)
        return dish
    
    async def update_dish(self, info: Info, dish_data: DishUpdateInput):
        async with info.context.db() as session:
            db_dish_by_name = await session.exec(select(Dish).where(Dish.name==dish_data.name))
            dish_by_name = db_dish_by_name.first()
            if dish_by_name and not dish_data.ingredients:
                raise DBObjectALreadyExistsError(
                    EXCEPTIONS["DISH"]["name_already_exists"]
                )
            db_dish = await session.exec(select(Dish).where(Dish.id==dish_data.id))
            dish = db_dish.first()
            if not dish:
                raise DBObjectNotFoundError(
                    EXCEPTIONS["DISH"]["id_does_not_exist"]
                )
            dish.name = dish_data.name
            dish.text = dish_data.text
            session.add(dish)
            await session.commit()
            await session.refresh(dish)
            if dish_data.ingredients:
                await self._delete_ingredient_amount(session, dish.id)
                for ingredient_data in dish_data.ingredients:
                    updated_ingredient = await self._update_dish_ingredient(session, ingredient_data.ingredient, dish.id)
                    if ingredient_data.amount:
                        await self._update_ingredient_amount(session, dish.id, updated_ingredient.id, ingredient_data.amount)
        return dish

    async def delete_dish(self, info: Info, dish_id: int):
        async with info.context.db() as session:
            db_dish = await session.exec(select(Dish).where(Dish.id==dish_id))
            dish = db_dish.first()
            if not dish:
                raise DBObjectNotFoundError(
                    EXCEPTIONS["DISH"]["id_does_not_exist"]
                )
            await self._delete_ingredient_amount(session, dish_id)
            await session.delete(dish)
            await session.commit()
    
        return dish

    async def _create_dish_ingredient(self, session: AsyncSession, ingredient_data: IngredientInput):
        db_ingredient = await session.exec(select(Ingredient).where(Ingredient.name==ingredient_data.name))
        ingredient = db_ingredient.first()
        if ingredient:
            return ingredient
        ingredient = Ingredient(
            name=ingredient_data.name,
            measure_unit=ingredient_data.measure_unit
        )
        session.add(ingredient)
        await session.commit()
        await session.refresh(ingredient)
        return ingredient

    async def _update_dish_ingredient(self, session: AsyncSession, ingredient_data: IngredientInput, dish_id: int):
        db_ingredient = await session.exec(select(Ingredient).where(Ingredient.name==ingredient_data.name))
        ingredient = db_ingredient.first()
        if ingredient:
            ingredient.measure_unit = ingredient_data.measure_unit
            session.add(ingredient)
            await session.commit()
            await session.refresh(ingredient)
            return ingredient
        return await self._create_dish_ingredient(session, ingredient_data)

    async def _create_ingredient_amount(self, session: AsyncSession, dish_id: int, ingredient_id: int, amount: int):
        ingredient_to_dish = DishIngredientAmount(dish_id=dish_id, ingredient_id=ingredient_id, amount=amount)
        session.add(ingredient_to_dish)
        await session.commit()
        await session.refresh(ingredient_to_dish)

    async def _update_ingredient_amount(self, session: AsyncSession, dish_id: int, ingredient_id: int, amount: int):
        db_ingredient_amount = await session.exec(
            select(DishIngredientAmount)
            .where(DishIngredientAmount.dish_id==dish_id, DishIngredientAmount.ingredient_id==ingredient_id)
        )
        ingredient_amount = db_ingredient_amount.first()
        if not ingredient_amount:
            await self._create_ingredient_amount(session, dish_id, ingredient_id, amount)
        else:
            ingredient_amount.amount = amount
            session.add(ingredient_amount)
            await session.commit()
            await session.refresh(ingredient_amount)

    async def _delete_ingredient_amount(self, session: AsyncSession, dish_id: int):
        db_ingredients_amount = await session.exec(
            select(DishIngredientAmount)
            .where(DishIngredientAmount.dish_id==dish_id)
        )
        ingredients_amount = db_ingredients_amount.all()
        for amount in ingredients_amount:
            await session.delete(amount)
            await session.commit()

