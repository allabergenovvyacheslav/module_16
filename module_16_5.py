# -*- coding: utf-8 -*-


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


@app.get('/users')
async def get_users() -> List[User]:
    return users


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