"""Collect observations requested by the lab; changes only this script's data."""
import json
import subprocess
import uuid
import requests

site = 'https://quickpizza.grafana.com'
with requests.Session() as s:
    def show(label, response):
        print(label, response.status_code, response.text)
        return response
    show('names', s.get(site + '/api/names', timeout=20))
    show('tools no token', s.get(site + '/api/tools', timeout=20))
    public = {'Authorization': 'token abcdef0123456789'}
    show('vegetarian', s.post(site + '/api/pizza', json={'mustBeVegetarian': True}, headers=public, timeout=20))
    user = {'username': 'lab-' + uuid.uuid4().hex[:12], 'password': 'Pizza-2026'}
    show('create user', s.post(site + '/api/users', json=user, timeout=20))
    auth = {'Authorization': 'token ' + s.post(site + '/api/users/token/login', json=user, timeout=20).json()['token']}
    pizza = s.post(site + '/api/pizza', json={}, headers=auth, timeout=20).json()['pizza']['id']
    for label, body in [('decimal', {'pizza_id': pizza, 'stars': 3.5}), ('text', {'pizza_id': pizza, 'stars': '3'}), ('missing', {'pizza_id': pizza}), ('pizza absent', {'pizza_id': 999999999, 'stars': 3})]:
        show(label, s.post(site + '/api/ratings', json=body, headers=auth, timeout=20))
    made = s.post(site + '/api/ratings', json={'pizza_id': pizza, 'stars': 3}, headers=auth, timeout=20).json()
    other = {'username': 'lab-' + uuid.uuid4().hex[:12], 'password': 'Pizza-2026'}
    s.post(site + '/api/users', json=other, timeout=20).raise_for_status()
    other_auth = {'Authorization': 'token ' + s.post(site + '/api/users/token/login', json=other, timeout=20).json()['token']}
    path = site + '/api/ratings/' + str(made['id'])
    try:
        for method in ('get', 'put', 'delete'):
            kwargs = {'headers': other_auth, 'timeout': 20}
            if method == 'put': kwargs['json'] = {'stars': 4}
            show('other ' + method, getattr(s, method)(path, **kwargs))
    finally:
        s.delete(path, headers=auth, timeout=20)
    show('all excluded', s.post(site + '/api/pizza', json={'excludedTools': ['Knife', 'Pizza cutter', 'Scissors']}, headers=auth, timeout=20))
print('made-up token curl:')
subprocess.run(['curl.exe', '-sS', '-i', '--max-time', '20', '-H', '@madeup.txt', site + '/api/ratings'], check=True)
