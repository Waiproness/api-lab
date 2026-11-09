import uuid
import pytest
import requests

SITE = 'https://quickpizza.grafana.com'
PUBLIC_AUTH = {'Authorization': 'token abcdef0123456789'}

class API(requests.Session):
    def request(self, method, url, **kwargs):
        kwargs.setdefault('timeout', 20)
        return super().request(method, SITE + url, **kwargs)

@pytest.fixture(scope='session')
def api():
    with API() as session:
        yield session

def log_in_new_user(api):
    user = {'username': 'lab-' + uuid.uuid4().hex[:12], 'password': 'Pizza-2026'}
    response = api.post('/api/users', json=user)
    assert response.status_code == 201, response.text
    response = api.post('/api/users/token/login', json=user)
    assert response.status_code == 200, response.text
    return {'Authorization': 'token ' + response.json()['token']}

@pytest.fixture
def auth(api):
    return log_in_new_user(api)

@pytest.fixture
def other_auth(api):
    return log_in_new_user(api)

@pytest.fixture
def pizza_id(api, auth):
    res = api.post('/api/pizza', json={}, headers=auth)
    assert res.status_code == 200, res.text
    return res.json()['pizza']['id']

@pytest.fixture
def rating(api, auth, pizza_id):
    res = api.post('/api/ratings', json={'pizza_id': pizza_id, 'stars': 3}, headers=auth)
    assert res.status_code == 201, res.text
    made = res.json()
    yield made
    api.delete(f"/api/ratings/{made['id']}", headers=auth)
