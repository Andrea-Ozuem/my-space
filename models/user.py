#!/usr/bin/python3
""" holds class User"""

from models.base_model import BaseModel
import models

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
    
    @property
    def tasks(self):
        tasks = models.storage.all(Tasks)
        task_list = [task for task in tasks.values if task.user_id == self.id]
        return task_list