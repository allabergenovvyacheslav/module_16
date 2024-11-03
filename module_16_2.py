# -*- coding: utf-8 -*-

# Задача "Аннотация и валидация":

# Допишите валидацию для маршрутов из предыдущей задачи при помощи классов Path и Annotated:

# '/user/{user_id}' - функция, выполняемая по этому маршруту, принимает аргумент user_id,
# для которого необходимо написать следующую валидацию:

# Должно быть целым числом
# Ограничено по значению: больше или равно 1 и меньше либо равно 100.
# Описание - 'Enter User ID'
# Пример - '1' (можете подставить свой пример не противоречащий валидации)

# '/user' замените на '/user/{username}/{age}' - функция, выполняемая по этому маршруту,
# принимает аргументы username и age, для которых необходимо написать следующую валидацию:

# username - строка, age - целое число.
# username ограничение по длине: больше или равно 5 и меньше либо равно 20.
# age ограничение по значению: больше или равно 18 и меньше либо равно 120.
# Описания для username и age - 'Enter username' и 'Enter age' соответственно.
# Примеры для username и age - 'UrbanUser' и '24' соответственно.


from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()


@app.get('/')
async def welcome() -> dict:
    return {'message': 'Главная страница'}


@app.get('/user/admin')
async def admin_panel() -> dict:
    return {'message': 'Вы вошли как администратор'}


@app.get('/user/{user_id}')
async def user_panel(
        user_id: Annotated[int, Path(
            ge=1,
            le=100,
            description='Enter User ID',
            example=1)]) -> dict:
    return {'message': f'Вы вошли как пользователь №{user_id}'}


@app.get('/user/{username}/{age}')
async def user_info(
        username: Annotated[str, Path(
            min_length=5,
            max_length=20,
            description='Enter username',
            example='UrbanUser')],
        age: int = Path(
            ge=18,
            le=120,
            description='Enter age',
            example=24)) -> dict:
    return {'message': f'Информация о пользователе. Имя: {username}, Возраст: {age}'}
