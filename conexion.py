import sqlite3
from sqlite3 import Error
from flask import g

DATABASES = 'db/acrimoto.db'

def get_db():
    try:
        if 'db' not in g:
            g.db=sqlite3.connect(DATABASES)
        return g.db
    except Error:
        print(Error)

def close_db():
    db = g.pop('db',None)
    if db is not None:
        db.close()
