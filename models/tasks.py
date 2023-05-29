#!/usr/bin/python3
""" holds class Tasks"""

from models.base_model import BaseModel

class Tasks(BaseModel):
    """Representation of a tasks """
    if models.storage_t == 'db':
        __tablename__ = 'tasks'
        description = Column(String(128), nullable=False)
        completed = Column(Boolean(create_constraint=True), nullable=False)
    else:
        description = ""
        completed = False

#if click on box 'jquery' turns to true both in file and db storage

    def __init__(self, *args, **kwargs):
        """initializes tasks"""
        super().__init__(*args, **kwargs)
