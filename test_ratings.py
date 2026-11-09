# A new rating contains its id, stars and pizza.
def test_create_rating(api, auth, pizza_id):
    res = api.post('/api/ratings', json={'pizza_id': pizza_id, 'stars': 5}, headers=auth)
    assert res.status_code == 201
    made = res.json()
    try:
        assert made['stars'] == 5 and made['pizza_id'] == pizza_id
        assert isinstance(made['id'], int)
    finally:
        api.delete(f"/api/ratings/{made['id']}", headers=auth)

# The owner can read a saved rating.
def test_read_rating(api, auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert res.status_code == 200
    assert res.json() == rating

# The owner can change a rating.
def test_update_rating(api, auth, rating):
    res = api.put(f"/api/ratings/{rating['id']}", json={'stars': 4}, headers=auth)
    assert res.status_code == 200
    assert res.json()['stars'] == 4

# A deleted rating is no longer found.
def test_delete_rating(api, auth, rating):
    path = f"/api/ratings/{rating['id']}"
    assert api.delete(path, headers=auth).status_code == 204
    assert api.get(path, headers=auth).status_code == 404
