#!/usr/bin/python3
from datetime import datetime
from models import storage
from models.user import User
from models.tasks import Tasks
from flask import Flask, render_template, redirect
from flask import request
import json
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
    try:
        description, temp, humidity, pressure, speed = get_weather(user)
    except TypeError:
        description = None
        temp = humidity = pressure = speed = 0
    away = get_time(user)

    now = datetime.now()
    home = now.strftime("%H:%M")

    return render_template('index.html',
                           user=user, total=len(tasks),
                           t_list=zip(tasks, range(len(tasks))),
                           done=len(done), t=temp, humid=humidity,
                           press=pressure, speed=speed,
                           summ=description, home=home,
                           city=user.city, away=away)

@app.route('/add/<u_id>', strict_slashes=False, methods=['POST'])
def post_task(u_id):
    'Sends a post request to api and renders updated page'
    url = 'http://0.0.0.0:5001/api/v1/users/{}/tasks'.format(u_id)
    headers = {
        "Content-Type": "application/json"
    }
    data = request.form.to_dict()
    data.update({'completed': 0})
    requests.post(url, json=data, headers=headers)
    print(type(data))
    return redirect('/')

def get_weather(user):
    # api = getenv('WEATHER_KEY', None)
    country = user.country
    city = user.city
    api = 'e6073d242a72d509b55819a4e455fb5f'
    endpoint = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&limit=1&appid={}'.format(city, country, api)
    try:
        r = requests.get(endpoint).json()
    except Exception:
        return
    name = r.get('name')
    description = r.get('weather')[0].get('description')
    temp = r.get('main').get('temp')
    humidity = r.get('main').get('humidity')
    pressure = r.get('main').get('pressure')
    speed = r.get('wind').get('speed')
    return (description, temp, humidity, pressure, speed)

def get_time(user):
    r = requests.get('https://timeapi.io/api/Time/current/zone?timeZone=Africa/Lagos').json()
    away = r.get('time')
    # do also for home
    return (away)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
