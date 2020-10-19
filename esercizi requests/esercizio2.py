import requests

                                                            #come inviare dei parametri con le nostre richisete
def get_rates(a,b):
                                                            #response = requests.get("https://api.exchangeratesapi.io/latest?base=USD&symbols=CAD")     
                                                            #l'url sopra mi indica anche eventuali parametri possibili da utilizzare per chiedere determinate valute
    payload = {"base": a, "symbols": b }                    #dati che richiedo al sito che in questo caso devono chiamarsi "base" e "symbols" perchè le api del sito lo pretendono
    response = requests.get("https://api.exchangeratesapi.io/latest", params = payload)
    if response.ok:                                         #nel caso in cui la richiesta va a buon fine
        data = response.json()                              #dati ricevuti dalla risposta in formato json
        print(data) 
        rate_date = data["date"]                            #prendo la data dai dati ricevuti
        exchange_rate = data ["rates"][b]                   #prendo il valore del cambio dai dati ricevuti
        print(f"1 {a} corrisponde a {exchange_rate} {b} il giorno {rate_date}")
    else:                                                   #nel caso in cui la richiesta non va a buon fine
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        raise Exception("c'è stato un errore...")

if __name__ == "__main__":
    a = "TRY"                                               #moneta turca
    b = "GBP"                                               #moneta britannica
    get_rates(a,b)