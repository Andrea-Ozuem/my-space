#!/usr/bin/python3
"""
initialize the models package
"""

from models.engine.file import FileStorage

storage = FileStorage()
storage.reload()
