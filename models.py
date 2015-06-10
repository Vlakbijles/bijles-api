#!/usr/bin/env python2
"""
    models.py, contains classes for declaring the SQLAlchemy models,
    these need to be synchronised with the SQL database used

    Models used (with their corresponding database table):
        Class           Database Table

        User        -   user
        UserMeta    -   user_meta
        Offer       -   offer
        Subject     -   subject
        Level       -   level
        Review      -   review

"""


from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Index
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Text
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
    meta = relationship("UserMeta", uselist=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.verified = False


class UserMeta(Base):
    __tablename__ = 'user_meta'

    id = Column("user_id", Integer, ForeignKey("user.id"), primary_key=True)
    name = Column("name", String(64))
    surname = Column("surname", String(64))
    postal_code = Column("postal_code", String(20))
    latitude = Column("latitude", DOUBLE)
    longitude = Column("longitude", DOUBLE)
    phone = Column("phone", String(10))
    photo_id = Column("photo_id", String(255))
    facebook_token = Column("facebook_token", String(255))
    description = Column(Text)


class Offer(Base):
    __tablename__ = "offer"

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey("user.id"))
    subject_id = Column('subject_id', Integer, ForeignKey("subject.id"))
    level_id = Column('level_id', Integer, ForeignKey("level.id"))

    # Define uniqueness of combination of columsn
    Index('user_id', 'subject_id', 'level_id', unique=True)

    # Relationships
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


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, ForeignKey("offer.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("user.id"))
    rating = Column(Integer)
    desc = Column(Text)
    create_date = Column(DateTime)

    offer = relationship("Offer", backref="review")
    author = relationship("User", backref="review")


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, ForeignKey("offer.id"), primary_key=True)

