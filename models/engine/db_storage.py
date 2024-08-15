#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.base_model import BaseModel, Base
from models.tasks import Tasks
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Tasks": Tasks
}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        DB_USER = getenv('DB_USER')
        DB_PWD = getenv('DB_PWD')
        DB_HOST = getenv('DB_HOST')
        DB_PORT = getenv('DB_PORT')
        DB_NAME = getenv('DB_NAME')
        self.__engine = create_engine('postgresql://{}:{}@{}:{}/{}'.
                                      format(DB_USER,
                                             DB_PWD,
                                             DB_HOST,
                                             DB_PORT,
                                             DB_NAME))

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        return self.__session.query(cls).filter(cls.id == id).first()

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

    def exists(self, cls, email):
        """
        Checks if a user exists
        """
        return self.__session.query(cls).filter(cls.email == email).first()
    
    def clear_completed(self, cls):
        """
        Deletes all completed tasks
        """
        tasks = self.__session.query(cls).filter(cls.completed == True).all()
        count = len(tasks)
        for task in tasks:
            self.delete(task)
        self.save()
        return count