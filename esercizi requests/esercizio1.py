import requests
from requests.exceptions import HTTPError

def get_jason(endpoint):
    response = requests.get(endpoint)
    if response.ok:
        json_data = response.json()
        return json_data
    else:
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        raise Exception("c'è stato un errore...")

def show_rates(data, currency):
    print("JSON data: ", data)
    rate_date = data["date"]
    exchange_rate = data ["rates"][currency]
    print(f"1 EUR corrisponde a {exchange_rate} {currency} il giorno {rate_date}")

if __name__ == "__main__":
    endpoint = "https://api.exchangeratesapi.io/latest"
    data = get_jason(endpoint)
    show_rates(data, "RON")