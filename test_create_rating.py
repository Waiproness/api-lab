import pytest

STARS_ERROR = 'number of stars must be between 1 and 5 (inclusive)'

# Base choice uses a real pizza, valid stars and the owner's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    res = api.post('/api/ratings', json={'pizza_id': pizza_id, 'stars': 3}, headers=auth)
    assert res.status_code == 201
    made = res.json()
    try:
        assert made['stars'] == 3 and made['pizza_id'] == pizza_id
    finally:
        api.delete(f"/api/ratings/{made['id']}", headers=auth)

# Values outside the permitted stars range are refused.
@pytest.mark.parametrize('stars', [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    res = api.post('/api/ratings', json={'pizza_id': pizza_id, 'stars': stars}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {'error': STARS_ERROR}

# Decimal, text and missing star values are refused.
@pytest.mark.parametrize(('stars', 'error'), [
    (3.5, 'json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int'),
    ('3', 'json: cannot unmarshal string into Go struct field Rating.stars of type int'),
    (None, STARS_ERROR),
], ids=['decimal', 'text', 'missing'])
def test_invalid_stars_type(api, auth, pizza_id, stars, error):
    body = {'pizza_id': pizza_id}
    if stars is not None:
        body['stars'] = stars
    res = api.post('/api/ratings', json=body, headers=auth)
    assert res.status_code == 400
    assert res.json() == {'error': error}

# A nonexistent pizza cannot be rated.
def test_nonexistent_pizza(api, auth):
    res = api.post('/api/ratings', json={'pizza_id': 999999999, 'stars': 3}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {'error': 'pizza ID 999999999 not found'}

# A missing or malformed token is refused.
@pytest.mark.parametrize('headers', [{}, {'Authorization': 'token short'}], ids=['missing', 'short'])
def test_invalid_token(api, pizza_id, headers):
    res = api.post('/api/ratings', json={'pizza_id': pizza_id, 'stars': 3}, headers=headers)
    assert res.status_code == 401
    assert res.json() == {'error': 'authentication failed'}
