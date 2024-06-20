import requests
res = requests.post('http://localhost:5000/api/create_app', json={"mytext":"lalala"})
if res.ok:
    print(res.json())