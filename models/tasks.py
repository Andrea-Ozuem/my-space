#!/usr/bin/python3
""" holds class Tasks"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Tasks(BaseModel, Base):
    """Representation of a tasks """
    if models.storage_t == "db":
        __tablename__ = 'tasks'
        user_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        description = Column(String(248), nullable=False)
        completed = Column(Boolean(create_constraint=True), nullable=False)
    else:
        user_id = ""
        description = ""
        completed = ""

    def __init__(self, *args, **kwargs):
        """initializes tasks"""
        super().__init__(*args, **kwargs)