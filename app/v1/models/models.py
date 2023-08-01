from sqlmodel import Field, Relationship, SQLModel


class DishIngredientAmount(SQLModel, table=True):

    """
    Таблица M-T-M для связи блюда и игредиента в БД
    с доп.полем количество
    для хранении информации о количестве игредиента в конкретном блюде
    """

    dish_id: int = Field(
        default=None,
        foreign_key='dish.id',
        primary_key=True,
    )
    ingredient_id: int = Field(
        default=None,
        foreign_key='ingredient.id',
        primary_key=True,
    )
    amount: int = Field(
        default=None,
        description='Количество ингредиента в блюде',
    )


class Dish(SQLModel, table=True):

    """Таблица Блюда в БД"""

    id: int = Field(
        default=None,
        primary_key=True,
        description='ID блюда',
    )
    name: str = Field(
        default=None,
        description='Название блюда',
        unique=True,
    )
    text: str | None = Field(
        default=None,
        description='Описание блюда',
    )
    ingredients: list['Ingredient'] | None | None = Relationship(
        back_populates='dishes',
        sa_relationship_kwargs={'lazy': 'selectin'},
        link_model=DishIngredientAmount,
    )


class Ingredient(SQLModel, table=True):

    """Таблица Ингредиента в БД"""

    id: int = Field(
        default=None,
        primary_key=True,
        description='ID ингредиента',
    )
    name: str = Field(
        default=None,
        description='Название ингредиента',
        unique=True,
    )
    measure_unit: str = Field(
        default=None,
        description='Единицы измерения',
    )
    dishes: list['Dish'] | None | None = Relationship(
        back_populates='ingredients',
        sa_relationship_kwargs={'lazy': 'selectin'},
        link_model=DishIngredientAmount,
    )
