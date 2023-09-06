#!/usr/bin/python3
import base64
from datetime import datetime, timedelta
from models import storage
from models.user import User
from models.tasks import Tasks
from flask import Flask, render_template, redirect, request, url_for, make_response
import urllib.parse as urlparse
import json
import requests
import os
import pytz
import secrets
import string

app = Flask(__name__)

CLIENT_ID = os.getenv('CLIENT_ID', None)
CLIENT_SECRET = os.getenv('CLIENT_SECRET', None)
REDIRECT_URI = "http://localhost:5000/callback"
TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
PROFILE_ENDPOINT = "https://api.spotify.com/v1/me"
CLIENT_CRED = CLIENT_ID + ':' + CLIENT_SECRET


user = storage.get(User, '00a11245-12fa-436e-9ccc-967417f8c30a')

state = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                for i in range(16))

@app.route('/flow', strict_slashes=False)
def flow():
    '''Flow endpoint for music recommendation'''
    if not user.is_auth:
        print('fail')
        return redirect('/login')
    token = user.token
    refresh = user.refresh
    expires = user.expires
    if expires < datetime.utcnow():
        print('expired')
        token = refresh_token(refresh)
    
    tracks = get_tracks(token)
    url = 'https://api.spotify.com/v1/recommendations'
    params = {
        'seed_artists': '4NHQUGzhtTLFvgF5SZesLK',
        'seed_genres': 'classical,country',
        'seed_tracks': '{},{}'.format(tracks[0], tracks[1]),
        'limit': 1
    }
    headers = {'Authorization': 'Bearer ' + token}
    res = requests.get(url, params=params, headers=headers)
    if res.status_code == 200:
        res = res.json()
        href = res.get('tracks')[0].get('external_urls').get('spotify')
        return redirect(href)
    else:
        return redirect('/')
    

@app.route('/deadline', strict_slashes=False)
def deadline():
    '''Deadline endpoint'''
    #handles
    token = spotify()
    tracks = get_tracks(token)
    limit = 1
    params = {
    'seed_artists': '4NHQUGzhtTLFvgF5SZesLK',
    'seed_genres': 'rock, samba',
    'seed_tracks': '{}, {}'.format(tracks[0], tracks[1])
    }
    headers = {'Authorization': 'Bearer ' + token}
    res = requests.get(url, params=params, headers=headers).json()
    href = res.get('tracks')[0].get('external_urls').get('href')
    return redirect(href)

def get_tracks(token):
    '''Get 2 User Saved Tracks'''
    limit = 2
    url = 'https://api.spotify.com/v1/me/tracks?limit={}'.format(limit)
    headers = {'Authorization': 'Bearer ' + token}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(res)
        return redirect('/')
    else:
        try:
            res = res.json()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    items = res.get('items')
    track_ids = [item.get('track').get('id') for item in items]
    return track_ids

@app.route('/login', strict_slashes=False)
def authorise():
    'request authorization from the user, so app can access the Spotify resources'
    scope = 'user-library-read'
    authorize_url = 'https://accounts.spotify.com/authorize?' + urlparse.urlencode({
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'state': state
    })
    return redirect(authorize_url)

@app.route('/callback', strict_slashes=False)
def callback():
    if len(request.args) > 0:
        code = request.args.get('code')
        req_state = request.args.get('state', None)
        if code is None or state != req_state:
            error_msg = {'error': 'state_mismatch'}
            make_response(jsonify(error_msg), 404)
            return response
        token = get_token(code)
        return redirect(url_for('main'))

def get_token(code):
    '''gets user access token/refresh token'''
    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'data': {
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        },
        'headers': {
            'authorization': 'basic ' + base64.b64encode((CLIENT_CRED).encode()).decode(),
            'content-type': 'application/x-www-form-urlencoded'
        },
        'json': True
    }
    response = requests.post(auth_options['url'], data=auth_options['data'], headers=auth_options['headers'])
    if response.status_code != 200:
        return redirect('/')
    res = response.json()
    token = res.get('access_token')
    refresh = res.get('refresh_token')
    expires = res.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires)
    update_tokens(token, expires, refresh)
    return token

def refresh_token(refresh):
    '''refreshes spotify access token'''
    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'data': {
            'grant_type': 'refresh_token',
            'refresh_token': refresh
        },
        'headers': {
            'authorization': 'basic ' + base64.b64encode((CLIENT_CRED).encode()).decode(),
        },
        'json': True
    }
    response = requests.post(auth_options['url'], data=auth_options['data'], headers=auth_options['headers'])
    if response.status_code != 200:
        return redirect('/') 
    res = response.json()
    token = res.get('access_token')
    expires = res.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires)
    update_tokens(token, expires, refresh)
    return token

@app.route('/', strict_slashes=False)
def main():
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
    home = pytz.timezone(user.tz1)
    home = datetime.now(home).strftime("%I:%M %p")
    away = pytz.timezone(user.tz2)
    away = datetime.now(away).strftime('%I:%M %p')
    return render_template('index.html',
                           user=user, total=len(tasks),
                           t_list=zip(tasks, range(len(tasks))),
                           done=len(done), t=temp, humid=humidity,
                           press=pressure, speed=speed,
                           summ=description, home=home,
                           city=user.city, away=away)

@app.route('/settings', strict_slashes=False)
def settings():
    '''Render settings page'''
    all_tz = pytz.all_timezones
    return render_template('setting.html',
                           user=user, all=all_tz)

def update_tokens(token, expires, refresh=None):
    '''Updates tokens on db'''
    #convert expires to isoformat to enable JSON serialisation
    formatted = expires.isoformat()
    url = 'http://0.0.0.0:5001/api/v1/users/{}'.format(user.id)
    headers = {
        "Content-Type": "application/json"
    }
    data = {'token': token, 'expires': formatted, 'refresh': refresh, 'is_auth': 1}
    r = requests.put(url, json=data, headers=headers)
    print(r.text)
    return redirect('/')


def get_weather(user):
    api = os.getenv('WEATHER_KEY', None)
    country = "Nigeria"
    city = user.city
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


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
