import strawberry
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.database import async_engine
from app.v1.models.models import Dish, DishIngredientAmount

# Resolvers


async def get_dish_ingredient_amount(
    root: 'DishType',
) -> list['DishIngredientAmountType']:
    """Резолвер для отображения количества ингредиента в блюде"""

    result = []

    async with AsyncSession(async_engine) as session:
        dish = await session.exec(select(Dish).where(Dish.id == root.id))
        dish_ingredients = dish.first().ingredients

        for ingredient in dish_ingredients:
            dish_ingredient_amount = await session.exec(
                select(DishIngredientAmount).where(
                    DishIngredientAmount.ingredient_id == ingredient.id,
                    DishIngredientAmount.dish_id == root.id,
                ),
            )
            amount = dish_ingredient_amount.first().amount
            result.append(
                DishIngredientAmountType(
                    id=ingredient.id,
                    name=ingredient.name,
                    measure_unit=ingredient.measure_unit,
                    amount=amount,
                ),
            )
    return result


# Types


@strawberry.type
class DishIngredientAmountType:
    id: int
    name: str
    measure_unit: str
    amount: int | None = None


@strawberry.type
class IngredientType:
    id: int
    name: str
    measure_unit: str


@strawberry.type
class DishType:
    id: int
    name: str
    text: str | None
    ingredients: list[DishIngredientAmountType] = strawberry.field(
        resolver=get_dish_ingredient_amount,
    )


@strawberry.type
class DishDeleteType:
    id: int
