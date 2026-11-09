import pytest

# Another user cannot read, change or delete the owner's rating.
@pytest.mark.parametrize('method', ['get', 'put', 'delete'])
def test_other_user_cannot_access(api, auth, other_auth, rating, method):
    path = f"/api/ratings/{rating['id']}"
    kwargs = {'headers': other_auth}
    if method == 'put':
        kwargs['json'] = {'stars': 4}
    res = getattr(api, method)(path, **kwargs)
    print(f'other-user {method}: {res.status_code} {res.text}')
    assert 400 <= res.status_code < 500
    owner = api.get(path, headers=auth)
    assert owner.status_code == 200
    assert owner.json() == rating
