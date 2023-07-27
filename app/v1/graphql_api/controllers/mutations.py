from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.database import async_engine
from app.v1.models.models import Dish, Ingredient, DishIngredientAmount
from app.v1.graphql_api.presentation.inputs import DishInput, DishUpdateInput, IngredientInput, IngredientUpdateInput


class CreateMutation:
    async def create_dish(self, dish_data: DishInput):
        async with AsyncSession(async_engine) as session:
            db_dish = await session.exec(select(Dish).where(Dish.name==dish_data.name))
            dish = db_dish.first()
            if dish:
                raise Exception("Блюдо с таким названием уже существует")
            dish = Dish(
                name=dish_data.name,
                text=dish_data.text
            )
            session.add(dish)
            await session.commit()
            await session.refresh(dish)
            for ingredient_data in dish_data.ingredients:
                new_ingredient = await self.create_ingredient(ingredient_data.ingredient, show_error=False)
                await self._create_ingredient_amount(dish.id, new_ingredient.id, ingredient_data.amount)
        return dish
    
    async def update_dish(self, dish_data: DishUpdateInput):
        async with AsyncSession(async_engine) as session:
            db_dish_by_name = await session.exec(select(Dish).where(Dish.name==dish_data.name))
            dish_by_name = db_dish_by_name.first()
            if dish_by_name and not dish_data.ingredients:
                raise Exception("Блюдо с таким  названием уже существует")
            db_dish = await session.exec(select(Dish).where(Dish.id==dish_data.id))
            dish = db_dish.first()
            if not dish:
                raise Exception("Блюдо с таким  id не существует")
            dish.name = dish_data.name
            dish.text = dish_data.text
            session.add(dish)
            await session.commit()
            await session.refresh(dish)
            if dish_data.ingredients:
                await self._delete_ingredient_amount(dish.id)
                for ingredient_data in dish_data.ingredients:
                    updated_ingredient = await self.update_dish_ingredient(ingredient_data.ingredient, dish.id)
                    if ingredient_data.amount:
                        await self._update_ingredient_amount(dish.id, updated_ingredient.id, ingredient_data.amount)
        return dish


    async def delete_dish(self, dish_id: int):
        async with AsyncSession(async_engine) as session:
            db_dish = await session.exec(select(Dish).where(Dish.id==dish_id))
            dish = db_dish.first()
            if not dish:
                raise Exception("Блюдо с таким  id не существует")
            await self._delete_ingredient_amount(dish_id)
            await session.delete(dish)
            await session.commit()
    
        return dish


    async def create_ingredient(self, ingredient_data: IngredientInput, show_error: bool = True):
        async with AsyncSession(async_engine) as session:
            db_ingredient = await session.exec(select(Ingredient).where(Ingredient.name==ingredient_data.name))
            ingredient = db_ingredient.first()
            if ingredient and not show_error:
                return ingredient
            elif ingredient and show_error:
                raise Exception("Ингредиент с таким названием уже существует")
            ingredient = Ingredient(
                name=ingredient_data.name,
                measure_unit=ingredient_data.measure_unit
            )
            session.add(ingredient)
            await session.commit()
            await session.refresh(ingredient)
        return ingredient

    
    async def update_dish_ingredient(self, ingredient_data: IngredientInput, dish_id: int):
        async with AsyncSession(async_engine) as session:
            db_ingredient = await session.exec(select(Ingredient).where(Ingredient.name==ingredient_data.name))
            ingredient = db_ingredient.first()
            if ingredient:
                ingredient.measure_unit = ingredient_data.measure_unit
                session.add(ingredient)
                await session.commit()
                await session.refresh(ingredient)
                return ingredient
            return await self.create_ingredient(ingredient_data, show_error=False)

    
    async def update_ingredient(self, ingredient_data: IngredientUpdateInput):
        async with AsyncSession(async_engine) as session:
            db_ingredient_by_name = await session.exec(select(Ingredient).where(Ingredient.name==ingredient_data.name))
            ingredient_by_name = db_ingredient_by_name.first()
            if ingredient_by_name:
                raise Exception("Ингредиент с таким названием уже существует")
            db_ingredient = await session.exec(select(Ingredient).where(Ingredient.id==ingredient_data.id))
            ingredient = db_ingredient.first()
            if not ingredient:
                raise Exception("Ингредиент с таким  id не существует")
            ingredient.name = ingredient_data.name
            ingredient.measure_unit = ingredient_data.measure_unit
            session.add(ingredient)
            await session.commit()
            await session.refresh(ingredient)
        return ingredient

    async def _create_ingredient_amount(self, dish_id: int, ingredient_id: int, amount: int):
        async with AsyncSession(async_engine) as session:
            ingredient_to_dish = DishIngredientAmount(dish_id=dish_id, ingredient_id=ingredient_id, amount=amount)
            session.add(ingredient_to_dish)
            await session.commit()
            await session.refresh(ingredient_to_dish)


    async def _update_ingredient_amount(self, dish_id: int, ingredient_id: int, amount: int):
        async with AsyncSession(async_engine) as session:
            db_ingredient_amount = await session.exec(
                select(DishIngredientAmount)
                .where(DishIngredientAmount.dish_id==dish_id, DishIngredientAmount.ingredient_id==ingredient_id)
            )
            ingredient_amount = db_ingredient_amount.first()
            if not ingredient_amount:
                await self._create_ingredient_amount(dish_id, ingredient_id, amount)
            else:
                ingredient_amount.amount = amount
                session.add(ingredient_amount)
                await session.commit()
                await session.refresh(ingredient_amount)


    async def _delete_ingredient_amount(self, dish_id: int):
        async with AsyncSession(async_engine) as session:
            db_ingredients_amount = await session.exec(
                select(DishIngredientAmount)
                .where(DishIngredientAmount.dish_id==dish_id)
            )
            ingredients_amount = db_ingredients_amount.all()
            for amount in ingredients_amount:
                await session.delete(amount)
                await session.commit()

