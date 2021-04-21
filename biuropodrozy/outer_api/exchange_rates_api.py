import requests


def get_rate_in_pln(currency):
    """Fetch rate in PLN from currency exchanges api"""

    response = requests.get(f"https://api.frankfurter.app/latest?from={currency}&to=PLN")
    rate = response.json()
    rate = rate['rates']['PLN']
    return {'rate_in_pln': rate}

def get_all_rates():
    """Fetch rates in PLN from currency exchanges api"""

    response = requests.get(f"https://api.frankfurter.app/latest?from=PLN")
    rates = response.json()
    rates = rates['rates']
    dict_keys = {}
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


