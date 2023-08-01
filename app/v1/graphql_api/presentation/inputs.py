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
    text: str
    ingredients: list['DishIngredientAmountInput']


@strawberry.input
class DishUpdateInput:
    id: int
    name: str
    text: str
    ingredients: list['DishIngredientAmountInput'] | None = None


@strawberry.input
class DishIngredientAmountInput:
    ingredient: IngredientInput
    amount: int


@strawberry.input
class IngredientsInput:
    ingredient_amount: list[DishIngredientAmountInput]
