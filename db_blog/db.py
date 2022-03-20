import os
import psycopg2


def db_connection():
    """ function to return db connection """
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='db_blog',
        user='flask',
        password='flask'
    )
    return conn
