#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from models.tasks import Tasks
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=True)
        city = Column(String(128), nullable=False)
        tz1 = Column(String(128), nullable=False)
        tz2 = Column(String(128), nullable=False, default="US/Central")
        is_auth = Column(Boolean, default=False, nullable=False)
        token = Column(String(256), nullable=True)
        refresh = Column(String(256), nullable=True)
        expires = Column(DateTime, nullable=True)
        artist = Column(String(64), nullable=False)
        tasks = relationship("Tasks", backref="user",
                              cascade="all, delete, delete-orphan")
        genres = relationship("Genres", backref="user",
                               cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
        country = ""
        city = ""
        fav_artist = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def tasks(self):
            tasks = models.storage.all(Tasks)
            task_list = [task for task in tasks.values() if task.user_id == self.id]
            return task_list
