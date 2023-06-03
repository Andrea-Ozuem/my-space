#!/usr/bin/python3
from datetime import datetime
from models import storage
from models.user import User
from models.tasks import Tasks
from flask import Flask, render_template
import requests
import os


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def main():
    user = storage.get(User, '00a11245-12fa-436e-9ccc-967417f8c30a')
    if os.getenv('STORAGE_TYPE', None) == 'db':
        tasks = user.tasks
    else:
        tasks = user.tasks()
    done = [task for task in tasks if task.completed == 1]
    description, temp, humidity, pressure, speed, away = get_weather(user)

    now = datetime.now()
    home = now.strftime("%H:%M")

    return render_template('index.html',
                           name=user.first_name,
                           tasks=tasks, total=len(tasks),
                           done=len(done), t=temp, humid=humidity, press=pressure, speed=speed, summ=description, home=home, away=away)

# Research o using external apis in  flask app

def get_weather(user):
    # api = getenv('WEATHER_KEY', None)
    country = user.country
    city = user.city
    api = 'e6073d242a72d509b55819a4e455fb5f'
    endpoint = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&limit=1&appid={}'.format(city, country, api)
    r = requests.get(endpoint).json()
    
    description = r.get('weather')[0].get('description')
    temp = r.get('main').get('temp')
    humidity = r.get('main').get('humidity')
    pressure = r.get('main').get('pressure')
    speed = r.get('wind').get('speed')
    return (description, temp, humidity, pressure, speed)
            
def get_time(user):
    time = requests.get('https://timeapi.io/api/Time/current/zone?timeZone=Africa/Lagos').json()
    time = r.get('time')
    # do also for home
    return (away, home)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)