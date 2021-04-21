import requests


def get_covid(country):
    """Fetch joke from joke API"""
    response = requests.get(f"https://api.covid19api.com/live/country/{country}/status/confirmed")
    covid = response.json()
    covid.reverse()
    today_covid = covid[0]['Active']

    return {"today_covid": today_covid}


'''@property - model
def results(self):
    covid = get_covid('poland')
    return covid'''

# <h1>{{model.results.today_covid}}</h1> - template

"""if '__main__' == __name__:
    res = get_covid('poland')
    print(res['today_covid'])"""

