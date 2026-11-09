import uuid

def new_user():
    return {'username': 'lab-' + uuid.uuid4().hex[:12], 'password': 'Pizza-2026'}

# Duplicate user names are refused.
def test_duplicate_username(api):
    user = new_user()
    assert api.post('/api/users', json=user).status_code == 201
    res = api.post('/api/users', json=user)
    assert res.status_code == 400
    assert res.json() == {'error': 'username already taken'}

# An incorrect password is refused.
def test_wrong_password(api):
    user = new_user()
    assert api.post('/api/users', json=user).status_code == 201
    res = api.post('/api/users/token/login', json={**user, 'password': 'incorrect'})
    assert res.status_code == 401
    assert res.json() == {'error': 'authentication failed'}

# An empty username is refused.
def test_empty_username(api):
    res = api.post('/api/users', json={'username': '', 'password': 'Pizza-2026'})
    assert res.status_code == 400
    assert res.json() == {'error': 'username field is empty'}
