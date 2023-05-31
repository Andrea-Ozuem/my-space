#!/usr/bin/python3
"""
initialize the models package
"""

import os

storage_t = os.getenv('STORAGE_TYPE', None)
if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file import FileStorage
    storage = FileStorage()
storage.reload()
