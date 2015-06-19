"""
    db.py
    Sets up database connection, includes SQLAlchemy boilerplate

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from config import db

db_uri = 'mysql://{user}:{password}@{host}/{name}?charset=utf8'.format(
                user=db['user'],
                password=db['password'],
                host=db['host'],
                name=db['name'])

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(db_uri))

session = scoped_session(Session)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance
