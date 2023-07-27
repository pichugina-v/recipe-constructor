from typing import List

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.v1.models.models import Dish, Ingredient, DishIngredientAmount
from app.v1.graphql_api.presentation.schemas import DishType, IngredientType
from app.db.database import async_engine



class Queries:
    async def get_all_dishes(self) -> List[DishType]:
        async with AsyncSession(async_engine) as session:
            db_dishes = await session.exec(select(Dish))
        return db_dishes.all()
    
    async def get_dish(self, dish_id: int) -> DishType:
        async with AsyncSession(async_engine) as session:
            db_dishes = await session.exec(select(Dish).where(Dish.id==dish_id))
        return db_dishes.first()
    
    async def get_all_ingredients(self) -> List[IngredientType]:
        async with AsyncSession(async_engine) as session:
            db_ingredients = await session.exec(select(Ingredient))
        return db_ingredients.all()
    
    async def get_ingredient(self, ingredient_id: int) -> IngredientType:
        async with AsyncSession(async_engine) as session:
            db_ingredients = await session.exec(select(Ingredient).where(Ingredient.id==ingredient_id))
        return db_ingredients.first()
