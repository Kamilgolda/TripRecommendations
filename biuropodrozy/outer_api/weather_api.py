import requests
import datetime


def get_weather(city_name):
    """Fetch joke from joke API"""
    response = requests.get(f"https://goweather.herokuapp.com/weather/{city_name}")
    weather = response.json()

    weekdays = ("Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela")
    today = datetime.datetime.now()
    next1day = today + datetime.timedelta(days=1)
    next2day = today + datetime.timedelta(days=2)
    next3day = today + datetime.timedelta(days=3)
    today = weekdays[today.weekday()]
    next1day = weekdays[next1day.weekday()]
    next2day = weekdays[next2day.weekday()]
    next3day = weekdays[next3day.weekday()]

    temp_today = f"{weather['temperature']}"
    desc_today = f"{weather['description']}"
    temp_next1day = f"{weather['forecast'][0]['temperature']}"
    temp_next2day = f"{weather['forecast'][1]['temperature']}"
    temp_next3day = f"{weather['forecast'][2]['temperature']}"
    return {"today_name": today,
            "next1day_name": next1day,
            "next2day_name": next2day,
            "next3day_name": next3day,
            "temp_today": temp_today,
            "desc_today": desc_today,
            "temp_next1day": temp_next1day,
            "temp_next2day": temp_next2day,
            "temp_next3day": temp_next3day}


'''@property - model
def results(self):
    weather = get_weather('warsaw')
    return weather'''

# <h1>{{model.results.today_name}}</h1> - template

'''if '__main__' == __name__:
    res = get_weather('rzeszow')
    print(res['today_name'])'''
