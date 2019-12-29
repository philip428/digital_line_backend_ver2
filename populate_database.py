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


# register client
payload = {
    "username": "yarik4",
    "password": "secret"
}

r = requests.post("http://127.0.0.1:5000/clients/register-and-login", json=payload)
load = r.json()
print(load)
token = load.get('token')
assert token is not None

# get in line
headers = {'Authorization': 'Bearer ' + token}

payload = {
    "line_name": "tst line"
}

r = requests.post("http://127.0.0.1:5000/clients/get-in-line", headers=headers, json=payload)
load = r.json()
print(load)

# register client
payload = {
    "username": "yarik5",
    "password": "secret"
}

r = requests.post("http://127.0.0.1:5000/clients/register-and-login", json=payload)
load = r.json()
print(load)
token = load.get('token')
assert token is not None

# get in line
headers = {'Authorization': 'Bearer ' + token}

payload = {
    "line_name": "tst line"
}

r = requests.post("http://127.0.0.1:5000/clients/get-in-line", headers=headers, json=payload)
load = r.json()
print(load)

# register client
payload = {
    "username": "yarik6",
    "password": "secret"
}

r = requests.post("http://127.0.0.1:5000/clients/register-and-login", json=payload)
load = r.json()
print(load)
token = load.get('token')
assert token is not None

# get in line
headers = {'Authorization': 'Bearer ' + token}

payload = {
    "line_name": "tst line"
}

r = requests.post("http://127.0.0.1:5000/clients/get-in-line", headers=headers, json=payload)
load = r.json()
print(load)


# call next
def call_next():
    headers = {'Authorization': 'Bearer ' + clerk_token}

    payload = {
        "line_name": "tst line"
    }

    r = requests.post("http://127.0.0.1:5000/clerks/call-next", headers=headers, json=payload)
    load = r.json()
    print(load)


i = input()

while i != "e":
    call_next()
    i = input()
