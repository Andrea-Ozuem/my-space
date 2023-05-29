#!/usr/bin/python3
""" holds class Genres"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship



class Genres(BaseModel, Base):
    """Representation of a genres """
    if models.storage_t == 'db':
        __tablename__ = 'genres'
        deadline= Column(String(128), nullable=False)
        flow = Column(String(128), nullable=False)
        user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    else:
        deadline = ""
        flow = ""
        user_id = ""
    def __init__(self, *args, **kwargs):
        """initializes genres"""
        super().__init__(*args, **kwargs)

class Artists(BaseModel, Base):
    """Representation of a artists """
    if models.storage_t == 'db':
        __tablename__ = 'artists'
        deadline= Column(String(128), nullable=False)
        flow = Column(String(128), nullable=False)
        user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    else:
        deadline = ""
        flow = ""
        user_id = ""
    def __init__(self, *args, **kwargs):
        """initializes genres"""
        super().__init__(*args, **kwargs)