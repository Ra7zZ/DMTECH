import requests

#il tutorial utilizza un server locale per testare il codice
#vedrò di riadattare il tutto se possibile
#altrimenti rimane come esempio per eventuali adattamenti futuri

def login(credentials):
    response = requests.post("http://127.0.0.1:8000/api/rest-auth/login/", data = credentials)

    if response.ok:
        print("Login success!")
        print(response.json())
        auth_token = response.json(['key'])
        return auth_token
    else:
        raise Exception("Errore. ", response.status_code)

def auth_request(endpoint, auth_token): #in questo esempio, il token di comunicazione viene inviato come header
    auth_header = f"Token {auth_token}"
    headers = {"Authorization": auth_header}

    response = requests.get(endpoint, headers = headers)
    if response.ok:
        response_data = response.json()
        print("Data: ", response_data)
    else:
        raise Exception("Errore. ", response.status_code)
      
if __name__ == "__main__":
    credentials = {"username": "neo", "password": "thereisnospoon"}
    auth_token = login(credentials)
    endpoint = "http://127.0.0.1:8000/api/rest-auth/login/"

    auth_request(endpoint, auth_token)