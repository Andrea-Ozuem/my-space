#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class User(BaseModel):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'user'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        country = Column(String(128), nullable=True)
        state = Column(String(128), nullable=True)
        fav_artist = Column(String(128), nullable=True)
        tasks = relationship("Tasks", backref="user",
                              cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
        country = ""
        state = ""
        fav_artist = ""
        
    def __init__(self, *args, **kwargs):
        """initializes user"""
    
    @property
    def tasks(self):
        tasks = models.storage.all(Tasks)
        task_list = [task for task in tasks.values if task.user_id == self.id]
        return task_list