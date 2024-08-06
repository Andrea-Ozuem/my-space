#!/usr/bin/python3
"""
initialize the models package
"""

import os
from dotenv import load_dotenv

load_dotenv()

storage_t = os.getenv('STORAGE_TYPE', None)
if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()

storage.reload()
