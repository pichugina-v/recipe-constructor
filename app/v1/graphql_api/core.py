from typing import List

import strawberry

from app.v1.graphql_api.controllers.mutations import CreateMutation
from app.v1.graphql_api.controllers.queries import Queries
from app.v1.graphql_api.presentation.schemas import DishType, DishDeleteType, IngredientType


@strawberry.type
class Mutation:
    create_ingredient: IngredientType = strawberry.mutation(resolver=CreateMutation().create_ingredient)
    update_ingredient: IngredientType = strawberry.mutation(resolver=CreateMutation().update_ingredient)
    create_dish: DishType = strawberry.mutation(resolver=CreateMutation().create_dish)
    update_dish: DishType = strawberry.mutation(resolver=CreateMutation().update_dish)
    delete_dish: DishDeleteType = strawberry.mutation(resolver=CreateMutation().delete_dish)


@strawberry.type
class Query:
    dishes: List[DishType] = strawberry.field(resolver=Queries().get_all_dishes)
    dish: DishType = strawberry.field(resolver=Queries().get_dish)
    ingredients: List[IngredientType] = strawberry.field(resolver=Queries().get_all_ingredients)
    ingredient: IngredientType = strawberry.field(resolver=Queries().get_ingredient)