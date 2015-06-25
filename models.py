#!/usr/bin/env python2
"""
    models.py
    Contains classes for declaring SQLAlchemy models

"""


from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Index
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    join_date = Column(DateTime)
    last_login = Column(DateTime)

    meta = relationship("UserMeta", uselist=False, backref="user")
    offers = relationship("Offer")
    token = relationship("Token", backref="user")

    def __repr__(self):
        return "<User(email='%s')>" % (self.email)


class UserMeta(Base):
    __tablename__ = 'user_meta'

    id = Column("user_id", Integer, ForeignKey("user.id"), primary_key=True)
    name = Column(String(64), nullable=False)
    surname = Column(String(64), nullable=False)
    age = Column(Integer)
    postal_code = Column(String(20))
    city = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    phone = Column(String(10))
    photo_id = Column(String(255), nullable=False)
    facebook_id = Column(String(255), nullable=False)
    description = Column(Text)

    def __repr__(self):
        return "<UserMeta(name='%s', surname='%s')>" % (self.name, self.surname)


class Offer(Base):
    __tablename__ = "offer"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    level_id = Column(Integer, ForeignKey('level.id'))
    active = Column(Boolean, default=True)

    # Define uniqueness of combination of columns
    Index('user_id', 'subject_id', 'level_id', unique=True)

    user = relationship("User")
    subject = relationship("Subject")
    level = relationship("Level")
    reviews = relationship("Review")

    def __repr__(self):
        return "<Offer(user_id='%d', subject_id='%d', level id='%d')>" % (
            self.user_id, self.subject_id, self.level_id)


class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)

    def __repr__(self):
        return "<Subject(id='%d', name='%s')>" % (self.id, self.name)


class Level(Base):
    __tablename__ = 'level'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)

    def __repr__(self):
        return "<Level(id='%d', name='%s')>" % (self.id, self.name)


class Review(Base):
    __tablename__ = 'review'

    offer_id = Column(Integer, ForeignKey("offer.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    endorsed = Column(Boolean, default=True)
    description = Column(Text)
    date = Column(DateTime)

    author = relationship("User")
    offer = relationship("Offer")

    def __repr__(self):
        return "<Author(offer_id='%d', author_id='%d', endorsed='%d')>" % (
            self.offer_id, self.author_id, self.endorsed)


class PostalCode(Base):
    __tablename__ = 'postal_code'

    id = Column(Integer, primary_key=True)
    postal_code = Column(String(7))
    postal_code_id = Column(Integer)
    city = Column(String(100))
    lat = Column(Float)
    lon = Column(Float)

    def __repr__(self):
        return "<PostalCode(postal_code='%s', city='%s')>" % (
            self.postal_code, self.city)


class Token(Base):
    __tablename__ = 'token'

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    hash = Column(String(255), unique=True, primary_key=True)
    create_date = Column(Integer, primary_key=True)

    def __repr__(self):
        return "<Token(user_id='%d', hash='%s')>" % (
            self.user_id, self.hash)
