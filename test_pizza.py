from conftest import PUBLIC_AUTH

# A vegetarian request returns a named pizza with vegetarian ingredients.
def test_vegetarian_pizza(api):
    res = api.post('/api/pizza', json={'mustBeVegetarian': True}, headers=PUBLIC_AUTH)
    assert res.status_code == 200
    pizza = res.json()['pizza']
    assert pizza['name']
    for ingredient in pizza['ingredients']:
        assert ingredient['vegetarian'] is True, ingredient['name']

# A request without a token is rejected.
def test_pizza_without_token_is_refused(api):
    res = api.post('/api/pizza', json={'mustBeVegetarian': True})
    assert res.status_code == 401
    assert res.json() == {'error': 'authentication failed'}
