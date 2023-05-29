#!/usr/bin/python3
""" holds class Tasks"""

from models.base_model import BaseModel

class Tasks(BaseModel):
    """Representation of a tasks """
    user_id = ""
    description = ""
    completed = ""

    def __init__(self, *args, **kwargs):
        """initializes tasks"""
        super().__init__(*args, **kwargs)