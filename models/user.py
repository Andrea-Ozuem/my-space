#!/usr/bin/python3
""" holds class User"""

from models.base_model import BaseModel
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

class User(BaseModel):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        fav_artist = Column(String(128), nullable=True)
        country = Column(String(128), nullable=True)
        state = Column(String(128), nullable=True)
        tasks = relationship("Tasks", backref="users",
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
        super().__init__(*args, **kwargs)
