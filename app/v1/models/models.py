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
    amount: int = Field(
        default=None,
        description="Amount of ingredient in dish"
    )

class Dish(SQLModel, table=True):
    id: int =  Field(
        default=None,
        primary_key=True,
        description="Dish ID"
    )
    name: str = Field(
        default=None,
        description="Dish name",
        unique=True,
    )
    text: Optional[str] = Field(
        default=None,
        description="Dish description"
    )
    ingredients:  Optional[List["Ingredient"] | None]= Relationship(
        back_populates='dishes',
        sa_relationship_kwargs={"lazy": "selectin"},
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
        description="Ingredient name",
        unique=True
    )
    measure_unit: str = Field(
        default=None,
        description="Ingredeint measurement unit"
    )
    dishes: Optional[List["Dish"] | None]  = Relationship(
        back_populates="ingredients",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=DishIngredientAmount
    )
    