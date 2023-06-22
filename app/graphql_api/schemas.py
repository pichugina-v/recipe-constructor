import strawberry

from typing import List, Optional


@strawberry.type
class DishIngredientAmount:
    id: int
    ingredient_id: int
    dish_id: int
    amount: int


@strawberry.type
class Ingredient:
    id: int
    name: str
    measure_unit: str


@strawberry.type
class Dish:
    id: int
    name: str
    text: str
    ingredients: List[DishIngredientAmount]
