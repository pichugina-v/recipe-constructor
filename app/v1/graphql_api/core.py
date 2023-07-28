from typing import List

import strawberry

from app.v1.graphql_api.controllers.mutations.dish_mutation import CreateDishMutation
from app.v1.graphql_api.controllers.mutations.ingredient_mutation import CreateIngredientMutation
from app.v1.graphql_api.controllers.queries.dish_queries import DishQueries
from app.v1.graphql_api.controllers.queries.ingredient_queries import IngredientQueries
from app.v1.graphql_api.presentation.schemas import DishType, DishDeleteType, IngredientType


@strawberry.type
class Mutation:
    create_ingredient: IngredientType = strawberry.mutation(resolver=CreateIngredientMutation().create_ingredient)
    update_ingredient: IngredientType = strawberry.mutation(resolver=CreateIngredientMutation().update_ingredient)
    create_dish: DishType = strawberry.mutation(resolver=CreateDishMutation().create_dish)
    update_dish: DishType = strawberry.mutation(resolver=CreateDishMutation().update_dish)
    delete_dish: DishDeleteType = strawberry.mutation(resolver=CreateDishMutation().delete_dish)


@strawberry.type
class Query:
    dishes: List[DishType] = strawberry.field(resolver=DishQueries().get_all_dishes)
    dish: DishType = strawberry.field(resolver=DishQueries().get_dish)
    ingredients: List[IngredientType] = strawberry.field(resolver=IngredientQueries().get_all_ingredients)
    ingredient: IngredientType = strawberry.field(resolver=IngredientQueries().get_ingredient)
