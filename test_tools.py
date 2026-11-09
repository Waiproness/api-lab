from conftest import PUBLIC_AUTH

# The public token permits reading all three tools.
def test_tools_are_listed(api):
    res = api.get('/api/tools', headers=PUBLIC_AUTH)
    assert res.status_code == 200
    assert res.json() == {'tools': ['Knife', 'Pizza cutter', 'Scissors']}
