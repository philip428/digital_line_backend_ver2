import requests

# register clerk
payload = {
    "username": "philip10",
    "password": "secret"
}

r = requests.post("http://127.0.0.1:5000/clerks/register-and-login", json=payload)
load = r.json()
print(load)
clerk_token = load.get('token')
assert clerk_token is not None

# create line
headers = {'Authorization': 'Bearer ' + clerk_token}

payload = {
    "line_name": "tst line"
}

r = requests.post("http://127.0.0.1:5000/clerks/create-line", headers=headers, json=payload)
load = r.json()
print(load)


def register_client(username):
    payload = {
        "username": "yarik5",
        "password": "secret"
    }

    r = requests.post("http://127.0.0.1:5000/clients/register-and-login", json=payload)
    load = r.json()
    print(load)
    token = load.get('token')
    assert token is not None
    return token

def get_in_line(token):
    headers = {'Authorization': 'Bearer ' + token}

    payload = {
        "line_name": "tst line"
    }

    r = requests.post("http://127.0.0.1:5000/clients/get-in-line", headers=headers, json=payload)
    load = r.json()
    print(load)


def call_next():
    headers = {'Authorization': 'Bearer ' + clerk_token}

    payload = {
        "line_name": "tst line"
    }

    r = requests.post("http://127.0.0.1:5000/clerks/call-next", headers=headers, json=payload)
    load = r.json()
    print(load)



def get_current_client():
    params = {"line_name": "tst line"}
    r = requests.get("http://127.0.0.1:5000/lines/get-current-client", params=params)
    load = r.json()
    print(load)

clients = []#['yarik1', 'yarik2', 'yarik3']

for c in clients:
    t = register_client(c)
    get_in_line(t)



i = input()

actions = {
    'cur': get_current_client,
    'n': call_next
}

while i != "e":
    actions.get(i)()
    i = input()
