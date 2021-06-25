import requests
from tenacity import retry, stop_after_attempt


@retry(stop=stop_after_attempt(3))
def fetch(url):
    """
       Pobranie adresu URl

       Args:
           url (string): adres url

       Returns:
           object: requests
       """
    return requests.get(url)


def get_rate_in_pln(currency):
    """Fetch rate in PLN from currency exchanges api

    Args:
        currency (string): waluta do przeliczenia

    Returns:
        object: Słownik z podaną walutą na PLN

    """
    rate = ""
    if currency != "PLN":
        response = fetch(f"https://api.frankfurter.app/latest?from={currency}&to=PLN")
        if response.ok:
            rate = response.json()
            rate = rate['rates']['PLN']
    return {'rate_in_pln': rate}


def get_all_rates():
    """Fetch rates in PLN from currency exchanges api

    Returns:
        object: Słownik z walutami na PLN

    """

    response = fetch(f"https://api.frankfurter.app/latest?from=PLN")
    dict_keys = {}
    if response.ok:
        rates = response.json()
        rates = rates['rates']
        for key in rates.keys():
            dict_keys[key]=get_rate_in_pln(key)['rate_in_pln']
    return dict_keys


'''@property - model
def results(self):
    rate_in_pln = get_rate_in_pln('USD')
    return rate_in_pln'''

# <h1>{{model.results.rate_in_pln}}</h1> - template

'''if '__main__' == __name__:
    res = get_rate_in_pln('USD')
    print(res['rate_in_pln'])
    print(get_all_rates())'''


