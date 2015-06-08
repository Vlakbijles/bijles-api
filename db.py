from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from config import CONFIG

db_uri = 'mysql://{user}:{password}@{host}/{name}'.format(
                user=CONFIG['db']['user'],
                password=CONFIG['db']['password'],
                host=CONFIG['db']['host'],
                name=CONFIG['db']['name'])

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(db_uri))
session = scoped_session(Session)
