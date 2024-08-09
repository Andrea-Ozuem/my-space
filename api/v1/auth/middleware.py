#!/usr/bin/env python3
"""
Authentication middleware
"""
from functools import wraps
from flask import abort, current_app, request
import jwt
from os import getenv
from models.user import User
from models import storage
from dotenv import load_dotenv
import requests

load_dotenv()

def token_required(f):
    """Checks if token is required"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        """Wrapper function"""
        auth_header = request.headers.get('Authorization')
        secret= getenv('JWT_SECRET')
        algo = getenv('ALGORITHM')
        if not auth_header:
            print('Error oo')
            abort(401)
        token = auth_header.split(" ")[1]
        try:
            data = jwt.decode(
                token, secret, algorithms=[algo]
            )
            current_user = storage.get(User, data.get('user_id'))
            if current_user is None:
                print('Error')
                abort(401)
        except jwt.ExpiredSignatureError:
            abort(400, 'Expired token')
        except jwt.InvalidTokenError:
            abort(400, 'Invalid token')
        except Exception:
            abort(401)
        return f(current_user, *args, **kwargs)

    return wrapper