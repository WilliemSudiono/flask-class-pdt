"""
File that contains the ORM definition using SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


# in order to use the connection we need to declare engine
# using urlstring 'postgresql://user:password@host/db_name'
# then bind the engine to session, so we do not have to connect to engine
engine = create_engine('postgresql://flask:flask@localhost/flask_petshop', future=True)
session = scoped_session(sessionmaker(autoflush=False, autocommit=False,
                                      bind=engine, future=True))


# then define a Base model to be used as a base
Base = declarative_base()
Base.query = session.query_property()


def close_session(exception=None):
    """ function to remove session """
    session.remove()


def init_db():
    """ function to initialize the database model """
    import petshop.models  # need to import all models here to declare table
    Base.metadata.create_all(bind=engine)


def init_app(app):
    """ helper function to pass into factory to remove session """
    app.teardown_appcontext(close_session)
