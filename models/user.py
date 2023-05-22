#!/usr/bin/python3
""" holds class User"""

from models.base_model import BaseModel

class User(BaseModel):
    """Representation of a user """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
    country = ""
    state = ""
    fav_artist = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
