from typing import Optional, List

import strawberry


@strawberry.input
class IngredientInput:
    name: str
    measure_unit: str


@strawberry.input
class IngredientUpdateInput:
    id: int
    name: str
    measure_unit: str


@strawberry.input
class DishInput:
    name: str
    text: Optional[str]
    ingredients: List["DishIngredientAmountInput"]


@strawberry.input
class DishUpdateInput:
    id: int
    name: str
    text: Optional[str]
    ingredients: Optional[List["DishIngredientAmountInput"]] = None


@strawberry.input
class DishIngredientAmountInput:
    ingredient: IngredientInput
    amount: int

