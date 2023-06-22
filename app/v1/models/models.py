from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship


class DishIngredientAmount(SQLModel, table=True):
    dish_id: int = Field(
        default=None,
        foreign_key="dish.id",
        primary_key=True
    )
    ingredient_id: int = Field(
        default=None,
        foreign_key="ingredient.id",
        primary_key=True
    )

class Dish(SQLModel, table=True):
    id: int =  Field(
        default=None,
        primary_key=True,
        description="Dish ID"
    )
    name: str = Field(
        default=None,
        description="Dish name"
    )
    text: Optional[str] = Field(
        default=None,
        description="Dish description"
    )
    ingredients: List["Ingredient"] = Relationship(
        back_populates='dishes',
        link_model=DishIngredientAmount
    )


class Ingredient(SQLModel, table=True):
    id: int =  Field(
        default=None,
        primary_key=True,
        description="Ingredient ID"
    )
    name: str = Field(
        default=None,
        description="Ingredient name"
    )
    measure_unit: str = Field(
        default=None,
        description="Ingredeint measurement unit"
    )
    dishes: List["Dish"] = Relationship(
        back_populates="ingredients",
        link_model=DishIngredientAmount
    )
    