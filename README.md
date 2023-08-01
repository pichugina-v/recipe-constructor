# Начало работы:

* Создайте файл `.env` и заполните переменные окружения из примера`.env.example`
* Запустите приложение
```bash
docker-compose up -d
```
* Для работы с данными используется эндпоинт `http://localhost:8000/graphql`

# Примеры запросов на API

* Запрос для получения всех блюд:

```python
query {
  dishes {
    id,
    name,
    text,
    ingredients {
      id
      name
      amount
    }
  }
}
```

* Запрос для получения всех блюд по ингредиентам:

```python
query {
  dishesByIngredients(
    ingredients: {ingredientAmount: [
      {ingredient: {name: "Фарш домашний", measureUnit: "гр"}, amount: 50},
      {ingredient: {name: "Сыр", measureUnit: "гр"}, amount: 150},
      {ingredient: {name: "Хлеб", measureUnit: "шт"}, amount: 5},
      {ingredient: {name: "Помидор", measureUnit: "шт"}, amount: 5},
    ]})
  {
      id
      name
      text
      ingredients {
        name
        measureUnit
        amount
      }
    }
  }
```

* Запрос для создания нового блюда:

```python
mutation {
  createDish(dishData: {
    name: "Тост",
    text: "Тост тепый с сыром",
    ingredients: [{
      amount: 20,
      ingredient: {
        name: "Сыр",
        measureUnit: "гр"
      }},
      {
        amount: 1,
        ingredient: {
          name: "Хлеб",
          measureUnit: "ломтик"
        }
      },
    ]
  })
  {
    id
    name
    text
    ingredients {
      id
      name
      measureUnit
      amount
    }
  }
}
```

* Запрос для удаления блюда:

```python
mutation {
  deleteDish(dishId: 1){
    id
  }
}
```
