#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Data(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'data'
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        home_tz = Column()
        foreign_tz = Column()
        fav_artist = Column(String(128), nullable=True)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def tasks(self):
            tasks = models.storage.all(Tasks)
            task_list = [task for task in tasks.values() if task.user_id == self.id]
            return task_list
