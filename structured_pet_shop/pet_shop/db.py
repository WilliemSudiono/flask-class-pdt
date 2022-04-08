from flask import g
import psycopg2


def db_connection():
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='flask_petshop',
        user='flask',
        password='flask'
    )
    return conn


# g is a special object that could be accessed for each request, it is similar
# to session
def get_db():
    if 'db' not in g:  # add connection if no db data found
        g.db = db_connection()
    return g.db


def close_db(e=None):
    db = g.pop('db', None)  # get db data from g object

    if db is not None:  # db data found, close the connection
        # by doing this, each time the response is delivered, db.close() is
        # called, so we do not need to call it each time we connect to db
        db.close()


def init_app(app):
    # teardown_appcontext is a special function that call the close_db function
    # each time the request is finished
    app.teardown_appcontext(close_db)
