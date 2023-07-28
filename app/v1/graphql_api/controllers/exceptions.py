EXCEPTIONS = {
    "DISH": {
        "id_does_not_exist": "Блюдо с таким id не существует",
        "name_already_exists": "Блюдо с таким  названием уже существует"
    },
    "INGREDIENT": {
        "id_does_not_exist": "Ингредиент с таким id не существует",
        "name_already_exists": "Ингредиент с таким  названием уже существует"
    }
}

class DBObjectNotFoundError(Exception):
    """Ошибка получения объекта из БД"""

    ...


class DBObjectALreadyExistsError(Exception):
    """Ошибка создания нового объекта в БД - объект уже существует"""

    ...
