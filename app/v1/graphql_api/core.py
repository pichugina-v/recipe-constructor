import strawberry

from app.v1.graphql_api.controllers.mutations.dish_mutation import DishMutation
from app.v1.graphql_api.controllers.mutations.ingredient_mutation import (
    IngredientMutation,
)
from app.v1.graphql_api.controllers.queries.dish_queries import DishQueries
from app.v1.graphql_api.controllers.queries.ingredient_queries import IngredientQueries
from app.v1.graphql_api.presentation.schemas import (
    DishDeleteType,
    DishType,
    IngredientType,
)


@strawberry.type
class Mutation:

    """Класс, отвечающий за подключение mutations для api"""

    create_ingredient: IngredientType = strawberry.mutation(
        resolver=IngredientMutation().create_ingredient,
    )
    update_ingredient: IngredientType = strawberry.mutation(
        resolver=IngredientMutation().update_ingredient,
    )
    create_dish: DishType = strawberry.mutation(
        resolver=DishMutation().create_dish,
    )
    update_dish: DishType = strawberry.mutation(
        resolver=DishMutation().update_dish,
    )
    delete_dish: DishDeleteType = strawberry.mutation(
        resolver=DishMutation().delete_dish,
    )


@strawberry.type
class Query:

    """Класс, отвечающий за подключение queries для api"""

    dishes: list[DishType] = strawberry.field(
        resolver=DishQueries().get_all_dishes,
    )
    dish: DishType = strawberry.field(resolver=DishQueries().get_dish)
    dishes_by_ingredients: list[DishType] = strawberry.field(
        resolver=DishQueries().get_dishes_by_ingredients,
    )
    ingredients: list[IngredientType] = strawberry.field(
        resolver=IngredientQueries().get_all_ingredients,
    )
    ingredient: IngredientType = strawberry.field(
        resolver=IngredientQueries().get_ingredient,
    )
