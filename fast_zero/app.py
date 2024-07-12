from http import HTTPStatus

from fastapi import (
    FastAPI,  # , Request, Response
)
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

templates = Jinja2Templates(directory='fast_zero/templates')

app = FastAPI()


# # Middleware para registrar os cabeçalhos de requisição e resposta
# @app.middleware('http')
# async def log_request_response(request: Request, call_next):
#     # Log dos cabeçalhos da requisição
#     print('Requisição:')
#     for header, value in request.headers.items():
#         print(f'{header}: {value}')

#     # Chamar o próximo middleware ou manipulador de rota
#     response = await call_next(request)

#     # Log dos cabeçalhos da resposta
#     print('Resposta:')
#     for header, value in response.headers.items():
#         print(f'{header}: {value}')

#     print('-' * 100)
#     print(request.headers)
#     print('-' * 100)
#     print(response.headers)
#     print('-' * 100)

#     return response


data_base = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo todo!'}


@app.post(
    '/users/',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
    response_class=JSONResponse,
)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(data_base) + 1, **user.model_dump())
    data_base.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=UserList)
def read_user():
    return {'users': data_base}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(data_base):
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    user_with_id = UserDB(id=user_id, **user.model_dump())
    data_base[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int):
    if user_id < 1 or user_id > len(data_base):
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    user = data_base[user_id - 1]
    del data_base[user_id - 1]
    return user


@app.get('/index', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('ola_mundo.html', {'request': request})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)
