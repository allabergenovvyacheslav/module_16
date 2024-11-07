# -*- coding: utf-8 -*-

# Задача "Список пользователей в шаблоне":

# Подготовка:

# Используйте код из предыдущей задачи.
# Скачайте заготовленные шаблоны для их дополнения.
# Шаблоны оставьте в папке templates у себя в проекте.
# Создайте объект Jinja2Templates, указав в качестве папки шаблонов - templates.

# Измените и дополните ранее описанные CRUD запросы:

# Напишите новый запрос по маршруту '/':
# Функция по этому запросу должна принимать аргумент request и возвращать TemplateResponse.
# TemplateResponse должен подключать ранее заготовленный шаблон 'users.html',
# а также передавать в него request и список users. Ключи в словаре для передачи определите
# самостоятельно в соответствии с шаблоном.

# Измените get запрос по маршруту '/user' на '/user/{user_id}':
# Функция по этому запросу теперь принимает аргумент request и user_id.
# Вместо возврата объекта модели User, теперь возвращается объект TemplateResponse.
# TemplateResponse должен подключать ранее заготовленный шаблон 'users.html',
# а также передавать в него request и одного из пользователей - user. Ключи в словаре для передачи
# определите самостоятельно в соответствии с шаблоном.

# Создайте несколько пользователей при помощи post запроса со следующими данными:
# username - UrbanUser, age - 24
# username - UrbanTest, age - 22
# username - Capybara, age - 60
# В шаблоне 'users.html' заготовлены все необходимые теги и обработка условий, вам остаётся только
# дополнить закомментированные строки вашим Jinja 2 кодом (использование полей id, username и age
# объектов модели User):


from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Annotated, List
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/')
async def get_all(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/users{user_id}')
async def get_users(request: Request,
                    user_id: Annotated[int, Path(
                        ge=0,
                        le=100,
                        description='Enter your user ID',
                        example='1')]) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id-1]})


@app.post('/user/{username}/{age}')
async def create_user(
        username: Annotated[str, Path(
            min_length=5,
            max_length=15,
            description='Enter your name',
            example='NewUser')],
        age: int = Path(
            ge=18,
            le=120,
            description='Enter age',
            example=24)) -> User:
    user_id = 1 if not users else users[-1].id + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_users(
        user_id: Annotated[int, Path(
            ge=0,
            le=100,
            description='Enter your user ID',
            example='1')],
        username: str = Path(
            min_length=5,
            max_length=15,
            description='Enter your name',
            example='NewUser'),
        age: int = Path(
            ge=18,
            le=120,
            description='Enter age',
            example=24)) -> User:
    try:
        for user in users:
            if user.id == user_id:
                user.username = username
                user.age = age
                return user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> User:
    try:
        for user in users:
            if user.id == user_id:
                users.remove(user)
                return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")