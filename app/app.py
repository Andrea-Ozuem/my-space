#!/usr/bin/python3
import base64
from datetime import datetime, timedelta
from models import storage
from models.user import User
from models.tasks import Tasks
from flask import Flask, render_template, redirect, request, url_for
import urllib.parse as urlparse
import json
import requests
import os
import secrets
import string

app = Flask(__name__)

user = storage.get(User, '00a11245-12fa-436e-9ccc-967417f8c30a')

state = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                for i in range(16))

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

def refresh_access_token(refresh):
    '''Refresh token'''
    client_cred = CLIENT_ID + ':' + CLIENT_SECRET
    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'data': {
            'grant_type': 'authorization_code',
            'refresh_token': refresh
        },
        'headers': {
            'Authorization': 'Basic ' + base64.b64encode((client_cred).encode()).decode(),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        'json': True
    }
    response = requests.post(auth_options['url'], data=auth_options['data'], headers=auth_options['headers'])
    res = response.json()
    token = res.get('access_token')
    expires = res.get('expires_in')
    now = datetime.now()
    expires = now + timedelta(seconds=expires)
    return token, expires
   
 
def get_token(client_id, code):
    'Callback to get Access Token'
    req_state = request.args.get('state', None)
    client_cred = CLIENT_ID + ':' + CLIENT_SECRET
    if req_state is None or state != req_state:
       return redirect(url_for('error', error='state_mismatch'))

    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'data': {
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        },
        'headers': {
            'Authorization': 'Basic ' + base64.b64encode((client_cred).encode()).decode(),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        'json': True
    }
    response = requests.post(auth_options['url'], data=auth_options['data'], headers=auth_options['headers'])
    res = response.json()
    print(res)
    token = res.get('access_token')
    if token in globals():
        print(token)
    refresh = res.get('refresh_token')
    expires = res.get('expires_in')
    now = datetime.now()
    expires = now + timedelta(seconds=expires)
    print(token)
    return token, refresh, expires


def get_user_info(token):
    '''Get 5 User Saved Tracks'''
    limit = 2
    url = 'https://api.spotify.com/v1/me/tracks?limit={}'.format(limit)
    headers = {'Authorization': 'Bearer ' + token}
    res = requests.get(url, headers=headers).json()
    items = res.get('items')
    track_ids = [item.get('track').get('id') for item in items]
    return track_ids

CLIENT_ID = os.getenv('CLIENT_ID', None)
CLIENT_SECRET = os.getenv('CLIENT_SECRET', None)
REDIRECT_URI = "http://localhost:5000/callback"
TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
PROFILE_ENDPOINT = "https://api.spotify.com/v1/me"

access_token = None
refresh_token = None
expires = datetime.fromtimestamp(0)

@app.route('/callback', strict_slashes=False)
def spotify_flow():
    global access_token
    global refresh_token
    code = request.args.get('code')
    if code is None:
        return redirect('/login')
    else:
        if refresh_token and expires < datetime.now():
            access_token, expires = refresh_access_token(refresh_token)
        elif refresh_token is None:
            print('code {}'.format(code))
            access_token, refresh_token, expires = get_token(CLIENT_ID, code)
        track_ids = get_user_info(access_token)
        print(track_ids)
        url = 'https://api.spotify.com/v1/recommendations'
        params = {
            'limit': 1,
            'seed_artists': '4NHQUGzhtTLFvgF5SZesLK',
            'seed_genres': 'classical, country',
            'seed_tracks': track_ids
        }
        headers = {'Authorization': 'Bearer ' + access_token}
        res = requests.get(url, params=params, headers=headers).json()
        tracks = res.get('tracks')
        href = [track.get('external_urls').get('spotify') for track in tracks]
        print(href)
        return redirect(href[0])


@app.route('/get_flow', strict_slashes=False)
def get_flow():
    '''Gets recommendation songs for both flow
    Redirects to song on Spotify'''
    ids = spotify_flow()
    print(ids.url)
    limit = 1
    params = {
    'seed_artists': '4NHQUGzhtTLFvgF5SZesLK',
    'seed_genres': 'classical, country',
    'seed_tracks': '{}, {}'.format(track_ids[0], track_ids[1])
    }
    headers = {'Authorization': 'Bearer ' + token}
    res = requests.get(url, params=params, headers=headers).json()
    href = res.get('tracks').get('external_urls').get('href')
    return redirect(href)


@app.route('/get_deadline', strict_slashes=False)
def get_deadline():
    '''Gets recommendation songs for both flow
    Redirects to song on Spotify'''
    track_seed = spotify_flow('deadline')
    print(track_seed)
    redirect('https://open.spotify.com/track/3rGBlf0cp7M3jbpsghlOH3')


@app.route('/', strict_slashes=False)
def main():
    if os.getenv('STORAGE_TYPE', None) == 'db':
        tasks = user.tasks
    else:
        tasks = user.tasks()
    done = [task for task in tasks if task.completed == 1]
    try:
        description, temp, humidity, pressure, speed = get_weather(user)
        away = get_time(user)
    except TypeError:
        description = None
        temp = humidity = pressure = speed = 0
        away = 0
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
    api = os.getenv('WEATHER_KEY', None)
    country = user.country
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
