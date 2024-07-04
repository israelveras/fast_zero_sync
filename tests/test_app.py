from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo todo!'}


# def test_retorna_html_em_index(client):
#     response = client.get('/index')
#     assert response.status_code == HTTPStatus.OK
#     assert response.headers['content-type'] == 'text/html; charset=utf-8'


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'password': 'password',
            'email': 'test@test.com',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'test',
        'email': 'test@test.com',
        'id': 1,
    }


def test_get_list_user(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'test',
                'email': 'test@test.com',
                'id': 1,
            }
        ]
    }
