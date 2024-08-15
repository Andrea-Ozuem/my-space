#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
auth_views = Blueprint('auth_views', __name__, url_prefix='/auth')
# spotify_views = Blueprint('spotify_views', __name__, url_prefix='/spotify')

from api.v1.views.user import *
from api.v1.views.tasks import *
from api.v1.views.auth import *
# from api.v1.views.spotify import *
