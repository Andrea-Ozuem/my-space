#!/usr/bin/python3
"""
initialize the models package
"""

from models.engine.file import FileStorage
import os

storage_t = os.getenv('STORAGE_TYPE', None)
storage = FileStorage()
storage.reload()
