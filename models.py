#!/usr/bin/env python2

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    # Columns
    id = Column('id', Integer, primary_key=True)
    email = Column('email', String(255), unique=True)
    password = Column('password', String(64))
    verified = Column('verified', Boolean)
    join_date = Column('join_date', DateTime)
    last_login = Column('last_login', DateTime)

    # Relationships
    offers = relationship("Offer")

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.verified = False


class Offer(Base):
    __tablename__ = "offer"

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey("user.id"))
    subject_id = Column('subject_id', Integer, ForeignKey("subject.id"))
    level_id = Column('level_id', Integer, ForeignKey("level.id"))

    subject = relationship("Subject")
    user = relationship("User")
    level = relationship("Level")


class Subject(Base):
    __tablename__ = 'subject'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64), nullable=False)


class Level(Base):
    __tablename__ = 'level'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64), nullable=False)
