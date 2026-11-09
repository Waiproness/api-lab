"""Collect the Step A2 error messages with curl and a private test user."""
import json
import subprocess
import tempfile
import uuid
from pathlib import Path

SITE = 'https://quickpizza.grafana.com'

with tempfile.TemporaryDirectory() as temp:
    directory = Path(temp)
    cookies = directory / 'cookies.txt'
    body_file = directory / 'body.json'
    header_file = directory / 'auth.txt'

    def call(path, body, header=None):
        body_file.write_text(json.dumps(body), encoding='utf-8')
        command = ['curl.exe', '-sS', '--max-time', '20', '-b', str(cookies),
                   '-c', str(cookies), '-H', 'Content-Type: application/json',
                   '-d', '@' + str(body_file), '-w', '\n%{http_code}', SITE + path]
        if header:
            header_file.write_text('Authorization: ' + header, encoding='utf-8')
            command[1:1] = ['-H', '@' + str(header_file)]
        output = subprocess.run(command, check=True, capture_output=True, text=True).stdout
        body_text, status = output.rsplit('\n', 1)
        return int(status), json.loads(body_text)

    user = {'username': 'lab-' + uuid.uuid4().hex[:12], 'password': 'Pizza-2026'}
    status, _ = call('/api/users', user)
    assert status == 201
    status, login = call('/api/users/token/login', user)
    assert status == 200
    auth = 'token ' + login['token']
    status, pizza = call('/api/pizza', {}, auth)
    assert status == 200
    pizza_id = pizza['pizza']['id']
    cases = [
        ('decimal', {'pizza_id': pizza_id, 'stars': 3.5}, auth),
        ('text', {'pizza_id': pizza_id, 'stars': '3'}, auth),
        ('missing stars', {'pizza_id': pizza_id}, auth),
        ('nonexistent pizza', {'pizza_id': 999999999, 'stars': 3}, auth),
        ('missing token', {'pizza_id': pizza_id, 'stars': 3}, None),
        ('short token', {'pizza_id': pizza_id, 'stars': 3}, 'token short'),
    ]
    for name, body, token in cases:
        status, response = call('/api/ratings', body, token)
        print(f'{name}: HTTP {status} {json.dumps(response)}')
