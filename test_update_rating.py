import pytest

# Boundaries are accepted or rejected, and the stored value is correct afterwards.
@pytest.mark.parametrize(('stars', 'status'), [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_boundaries(api, auth, rating, stars, status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={'stars': stars}, headers=auth)
    assert res.status_code == status
    read = api.get(path, headers=auth)
    assert read.status_code == 200
    assert read.json()['stars'] == (stars if status == 200 else 3)
