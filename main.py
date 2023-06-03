#!/usr/bin/python3

from models.user import User
import models
import requests

def get_weather(user):
    # api = getenv('WEATHER_KEY', None)
    country = user.country
    city = user.city
    api = 'e6073d242a72d509b55819a4e455fb5f'
    endpoint = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&limit=1&appid={}'.format(city, country, api)
    r = requests.get(endpoint).json()
    print(r)
    description = r.get('weather')[0].get('description')
    temp = r.get('main').get('temp')
    humidity = r.get('main').get('humidity')
    pressure = r.get('main').get('pressure')
    speed = r.get('wind').get('speed')
    print(temp, humidity, pressure, speed)
    return (temp, humidity, pressure, speed)

if __name__ == "__main__":
    get_weather(models.storage.get(User, 'b5dfebcd-2f1d-4d19-b266-8f58f37b4aa5'))
