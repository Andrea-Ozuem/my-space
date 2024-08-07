#!/usr/bin/python3
""" holds class User"""

from os import getenv
import datetime as dt
from passlib.context import CryptContext
import sqlalchemy
import jwt
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship

import models
from models.base_model import BaseModel, Base
from models.tasks import Tasks

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel, Base):
    """Representation of a user """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=True)
    city = Column(String(128), nullable=True)
    tz2 = Column(String(128), nullable=True)
    tz1 = Column(String(128), nullable=True, default="US/Central")
    tasks = relationship("Tasks", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def hash_password(self, pwd):
        """hashes password"""
        hashed_password = pwd_context.hash(secret=pwd)
        return hashed_password

    def verify_password(self, password: str, hash: str) -> bool:
        """Function to verify a hashed password"""
        return pwd_context.verify(secret=password, hash=hash)
    
    def create_access_token(self, user_id):
        """creates access token"""
        secret= getenv('JWT_SECRET')
        algo = getenv('ALGORITHM')
        expires = dt.datetime.now(dt.timezone.utc) + dt.timedelta(
            hours=24
        )
        data = {"user_id": user_id, "exp": expires}
        encoded_jwt = jwt.encode(data, secret, algo)
        return encoded_jwt