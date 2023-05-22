#!/usr/bin/python3
""" holds class Genres"""

from models.base_model import BaseModel

class Music(BaseModel):
    """Basemodel for music recommendation system"""
    deadline = ""
    flow = ""
    user_id = ""
    
class Genres(Music):
    """Representation of a genres """
    def __init__(self, *args, **kwargs):
        """initializes genres"""
        super().__init__(*args, **kwargs)

class Artists(Music):
    """Representation of a artists """
    def __init__(self, *args, **kwargs):
        """initializes genres"""
        super().__init__(*args, **kwargs)
