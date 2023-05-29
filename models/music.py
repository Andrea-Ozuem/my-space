#!/usr/bin/python3
""" holds class Genres"""

from models.base_model import BaseModel
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

    
class Genres(BaseModel, Base):
    """Representation of a genres """
    if models.storage_t == 'db':
        __tablename__ = 'genres'
        deadl ine= Column(String(128), nullable=False)
        flow = Column(String(128), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
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
        deadl ine= Column(String(128), nullable=False)
        flow = Column(String(128), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        deadline = ""
        flow = ""
        user_id = ""
    def __init__(self, *args, **kwargs):
        """initializes genres"""
        super().__init__(*args, **kwargs)
