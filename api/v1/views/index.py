#!/usr/bin/python3

import base64
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, request, url_for, make_response, session
import urllib.parse as urlparse
import json
import requests
import os
import pytz
from dotenv import load_dotenv

from models import storage
from models.user import User
from models.tasks import Tasks
from api.v1.auth.middleware import token_required
from api.v1.api import app
from api.v1.views import app_views

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID', None)
CLIENT_SECRET = os.getenv('CLIENT_SECRET', None)
REDIRECT_URI = "http://localhost:5000/callback"
TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
PROFILE_ENDPOINT = "https://api.spotify.com/v1/me"

@app_views.route('/', methods=['GET'], strict_slashes=False)
@token_required
def main(current_user: User):
    tasks = current_user.tasks
    done = [task for task in tasks if task.completed == 1]
    try:
        description, temp, humidity, pressure, speed = get_weather(current_user)
    except TypeError:
        description = None
        temp = humidity = pressure = speed = 0
   
    home = datetime.now().strftime("%I:%M %p") 
    away = pytz.timezone(f'{current_user.tz1}')
    away = datetime.now(away).strftime('%I:%M %p')
    return render_template('index.html',
                           user=current_user, total=len(tasks),
                           t_list=zip(tasks, range(len(tasks))),
                           done=len(done), t=temp, humid=humidity,
                           press=pressure, speed=speed,
                           summ=description, home=home,
                           city=current_user.city, away=away)


def get_weather(user: User):
    api = os.getenv('WEATHER_KEY', None)
    city = user.city
    if city:
        endpoint = 'https://api.openweathermap.org/data/2.5/weather?q={}&limit=1&appid={}'.format(city, api)
    else:
        if request.headers.getlist("X-Forwarded-For"):
            user_ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            user_ip = request.remote_addr
        IP_KEY = os.getenv('IP_KEY', None)
        url = f'https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey={IP_KEY}&ipAddress={user_ip}'
        geoip_data = requests.get(url).json()
        lat = geoip_data['location']['lat']
        lon = geoip_data['location']['lng']
        endpoint = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'.format(lat, lon,api)
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


@app.route('/add/<u_id>', strict_slashes=False, methods=['POST'])
@token_required
def update_task(u_id):
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
