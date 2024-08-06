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
        city = Column(String(128), nullable=True)
        tz1 = Column(String(128), nullable=True)
        tz2 = Column(String(128), nullable=True, default="US/Central")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)