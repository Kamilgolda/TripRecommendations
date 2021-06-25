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


def get_covid(country):
    """Fetch covid cases from covid API

    Args:
        country (string): nazwa kraju

    Returns:
        object: Zwraca słownik z zarazeniami w podanym kraju

    """
    response = fetch(f"https://api.covid19api.com/live/country/{country}/status/confirmed")
    if response.ok:
        covid = response.json()
        covid.reverse()
        today_covid = covid[0]['Active']
    else:
        today_covid = "Brak informacji"

    return {"today_covid": today_covid}


'''@property - model
def results(self):
    covid = get_covid('poland')
    return covid'''

# <h1>{{model.results.today_covid}}</h1> - template

"""if '__main__' == __name__:
    res = get_covid('poland')
    print(res['today_covid'])"""
