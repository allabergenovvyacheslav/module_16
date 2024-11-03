from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def welcome() -> dict:
    return {'message': 'Главная страница'}


@app.get('/user/admin')
async def admin_panel() -> dict:
    return {'message': 'Вы вошли как администратор'}


@app.get('/user/{user_id}')
async def user_panel(user_id: int = 123) -> dict:
    return {'message': f'Вы вошли как пользователь №{user_id}'}


@app.get('/user')
async def user_info(user: str, age: int) -> dict:
    return {'message': f'Информация о пользователе. Имя: {user}, Возраст: {age}'}