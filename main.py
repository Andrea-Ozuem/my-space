#!/usr/bin/python3

from models.user import User
import models

user = models.storage.all(User)
for u in user.values():
    for task in list(u.tasks):
        print(task.description)
